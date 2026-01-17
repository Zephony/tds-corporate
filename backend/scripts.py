import os
import re
import sys
import json
import click
import inspect
import pandas as pd
import time

from datetime import datetime, timedelta, time as time_of_day
import bcrypt
from sqlalchemy import inspect as sa_inspect, select, delete, text

from backend.database import engine, SessionLocal, Base
from backend.helpers import unflatten_json, camel_case_to_words, to_snake_case
from backend.models import *

# Using bcrypt directly for password hashing

# Terminal control utilities for dynamic output
class ProgressDisplay:
    """Utility class for dynamic terminal output"""
    _last_update_time = 0
    _last_progress_text = ""
    
    @staticmethod
    def clear_line():
        """Clear the current line"""
        if sys.stdout.isatty():  # Only use ANSI codes if we're in a terminal
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
    
    @staticmethod
    def update_line(text):
        """Update the current line with new text"""
        if sys.stdout.isatty():  # Only use ANSI codes if we're in a terminal
            # Move to beginning of line, clear it, and write new text
            sys.stdout.write(f'\r{text}\033[K')
            sys.stdout.flush()
        else:
            # Fallback for non-terminal environments
            print(text)
    
    @staticmethod
    def finalize_line(text):
        """Finalize the current line and move to next line"""
        if sys.stdout.isatty():
            ProgressDisplay.clear_line()
        print(text)
        # Reset progress tracking variables
        ProgressDisplay._last_update_time = 0
        ProgressDisplay._last_progress_text = ""
    
    @staticmethod
    def show_progress(current, total, prefix="Processing", item_name="items"):
        """Show a progress indicator"""
        # For very small datasets, don't show progress bar - just show completion
        if total <= 10:
            if current == total:
                print(f"{prefix} {total} {item_name}... completed")
            return
        
        # For larger datasets, only show at meaningful intervals
        update_interval = max(1, total // 5)  # Show 5 updates maximum
        
        if current == 1 or current == total or current % update_interval == 0:
            percentage = (current / total) * 100 if total > 0 else 0
            bar_length = 20  # Shorter bar to reduce terminal issues
            filled_length = int(bar_length * current // total) if total > 0 else 0
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            if sys.stdout.isatty() and current < total:
                # Only show progress bar for intermediate updates
                sys.stdout.write(f'\r{prefix}: [{bar}] {current}/{total} {item_name} ({percentage:.0f}%)')
                sys.stdout.flush()
            elif current == total:
                # Final update - show 100% progress bar and keep it
                if sys.stdout.isatty():
                    sys.stdout.write(f'\r{prefix}: [{bar}] {current}/{total} {item_name} ({percentage:.0f}%)')
                    sys.stdout.flush()
                    print()  # Move to next line but keep the progress bar visible
                else:
                    print(f"{prefix}: [{bar}] {current}/{total} {item_name} ({percentage:.0f}%)")
            else:
                # Non-terminal fallback
                print(f"{prefix}: [{bar}] {current}/{total} {item_name} ({percentage:.0f}%)")
    
    @staticmethod
    def show_counter(current, prefix="Processing", item_name="items"):
        """Show a simple counter"""
        ProgressDisplay.update_line(f"{prefix}: {current} {item_name}...")

@click.group()
def cli():
    pass


def get_field_type_from_column(column_info):
    """Determine the field type from a SQLAlchemy column info dict"""
    type_name = str(column_info['type']).lower()
    
    if 'int' in type_name:
        return 'integer'
    elif 'float' in type_name or 'numeric' in type_name or 'decimal' in type_name:
        return 'float'
    elif 'bool' in type_name:
        return 'boolean'
    elif 'date' in type_name and 'time' not in type_name:
        return 'date'
    elif 'datetime' in type_name or 'timestamp' in type_name:
        return 'datetime'
    elif 'json' in type_name:
        return 'json'
    elif 'text' in type_name:
        return 'text'
    else:
        return 'string'


def get_display_type_from_field_type(field_type):
    """Determine the display type from field type"""
    mapping = {
        'string': 'text',
        'integer': 'number',
        'float': 'number',
        'boolean': 'checkbox',
        'date': 'date',
        'datetime': 'datetime',
        'json': 'json_editor',
        'text': 'textarea',
    }
    return mapping.get(field_type, 'text')


def extract_field_metadata_from_sqlalchemy(model_class, field_name):
    """Extract metadata from SQLAlchemy field if available"""
    try:
        # Get the mapped column from the model class
        if hasattr(model_class, field_name):
            field_attr = getattr(model_class, field_name)
            
            # For SQLAlchemy 2.0 mapped_column syntax
            if hasattr(field_attr, 'property') and hasattr(field_attr.property, 'columns'):
                column = field_attr.property.columns[0]
                
                # In SQLAlchemy, the metadata parameter becomes the info attribute
                if hasattr(column, 'info') and column.info:
                    return column.info
                    
        return {}
    except Exception as e:
        print(f"Warning: Could not extract metadata for field {field_name}: {e}")
        return {}


def populate_metadata_tables():
    """Automatically populate metadata tables based on all existing models"""
    
    # Get all model classes from the current module (since we imported with *)
    all_models = []
    
    # Get all models from the current module's namespace
    current_module = sys.modules[__name__]
    for name in dir(current_module):
        obj = getattr(current_module, name)

        inherited_from_base_model = inspect.isclass(obj) and issubclass(obj, BaseModel) and obj != BaseModel
        has_table_name = hasattr(obj, '__tablename__')
        if inherited_from_base_model and has_table_name:
            all_models.append(obj)
    
    # Filter out metadata models to avoid circular references
    metadata_models = [MetadataObject, MetadataField, MetadataRelationship]
    non_metadata_models = [model for model in all_models if model not in metadata_models]
    
    db_session = SessionLocal()
    try:
        # Clear existing metadata using SQLAlchemy 2.0+ syntax
        db_session.execute(delete(MetadataRelationship))
        db_session.execute(delete(MetadataField))
        db_session.execute(delete(MetadataObject))
        db_session.commit()
        
        # Create metadata objects for each model
        metadata_objects = {}
        print(f"Creating metadata objects for {len(non_metadata_models)} models...")
        
        for index, model_class in enumerate(non_metadata_models):
            if not hasattr(model_class, '__tablename__'):
                continue
            
            ProgressDisplay.show_progress(index + 1, len(non_metadata_models), "Creating metadata objects", "models")
                
            table_name = model_class.__tablename__
            class_name = model_class.__name__
            token = model_class.__table__.info.get('token', to_snake_case(class_name))
            name = model_class.__table__.info.get('name', class_name)
            description = model_class.__table__.info.get('description')
            object_type = model_class.__table__.info.get('type', 'table')
            can_login = model_class.__table__.info.get('can_login', False)
            api_configuration = model_class.__table__.info.get('api', {})
            
            # Create metadata object
            metadata_object = MetadataObject(
                token=token,
                name=name,
                description=description,
                object_type=object_type,
                table_name=table_name,
                model_class=class_name,
                is_active=True,
                is_system=False,
                is_read_only=False,
                can_login=can_login,
                configuration={},
                api_configuration=api_configuration,
            )
            db_session.add(metadata_object)
            db_session.flush()  # Get the ID
            metadata_objects[class_name] = metadata_object
        
        ProgressDisplay.finalize_line(f"Created metadata objects for {len(metadata_objects)} models")
        
        # Create metadata fields for each model
        print(f"\nProcessing fields for {len(non_metadata_models)} models...")
        total_fields = 0
        fields_with_metadata = 0
        
        for model_class in non_metadata_models:
            if not hasattr(model_class, '__tablename__'):
                continue
                
            class_name = model_class.__name__
            metadata_object = metadata_objects.get(class_name)
            if not metadata_object:
                continue
            
            # Get table columns
            try:
                inspector = sa_inspect(engine)
                table_name = model_class.__tablename__
                columns = inspector.get_columns(table_name)
            except Exception as e:
                print(f"Warning: Could not inspect table {table_name} for {class_name}: {e}")
                continue
            
            # Get model attributes
            model_attrs = {}
            for attr_name in dir(model_class):
                attr = getattr(model_class, attr_name)
                if hasattr(attr, 'type'):
                    model_attrs[attr_name] = attr
            
            # Create metadata fields
            display_order = 0
            model_fields_with_metadata = 0
            
            for column in columns:
                column_name = column['name']
                
                # Skip certain columns
                if column_name in ['id', 'created_at', 'updated_at']:
                    continue
                
                # Get field type
                field_type = get_field_type_from_column(column)
                display_type = get_display_type_from_field_type(field_type)
                
                # Determine if it's a foreign key
                is_foreign_key = False
                if column_name.startswith('id_'):
                    is_foreign_key = True
                    field_type = 'foreign_key'
                
                # Try to get metadata from SQLAlchemy field first
                field_metadata = extract_field_metadata_from_sqlalchemy(model_class, column_name)
                if field_metadata:
                    model_fields_with_metadata += 1
                    fields_with_metadata += 1
                    ProgressDisplay.update_line(f"    Finding metadata: {class_name}.{column_name} (found {fields_with_metadata} fields with metadata)")
                
                # Create display name
                display_name = field_metadata.get(
                    'display_name',
                    column_name.replace('_', ' ').title(),
                )
                
                # Get description
                description = field_metadata.get(
                    'description',
                    f"Field {display_name} for {class_name}",
                )
                
                # Override display_type if available in metadata
                display_type = field_metadata.get(
                    'display_type',
                    get_display_type_from_field_type(field_type),
                )
                
                # Determine field properties
                is_primary_key = column.get('primary_key', False)
                is_nullable = column.get('nullable', True)
                is_unique = column.get('unique', False)
                
                # Use metadata values if available, otherwise use sensible defaults
                is_visible = field_metadata.get('is_visible', True)
                is_searchable = field_metadata.get('is_searchable', False)
                is_sortable = field_metadata.get('is_sortable', True)
                is_filterable = field_metadata.get('is_filterable', False)
                is_initializable = field_metadata.get('is_initializable', True)
                is_editable = field_metadata.get('is_editable', True)
                is_required = field_metadata.get('is_required', not is_nullable)
                
                # Prepare additional metadata fields
                validation_rules = field_metadata.get('validation_rules', {}) if field_metadata else {}
                display_settings = field_metadata.get('display_settings', {}) if field_metadata else {}
                help_text = field_metadata.get('help_text', '') if field_metadata else ''
                
                # text fields have min/max length, numbers have min/max value
                min_length = field_metadata.get('min_length', None)
                max_length = field_metadata.get('max_length', None)
                min_value = field_metadata.get('min_value', None)
                max_value = field_metadata.get('max_value', None)
                
                # Create metadata field with all available information
                metadata_field = MetadataField(
                    name=column_name,
                    display_name=display_name,
                    description=description,
                    field_type=field_type,
                    display_type=display_type,
                    column_name=column_name,
                    column_type=str(column['type']),
                    is_nullable=is_nullable,
                    is_primary_key=is_primary_key,
                    is_unique=is_unique,
                    is_indexed=False,  # Would need to check indexes separately
                    is_visible=is_visible,
                    is_initializable=is_initializable,
                    is_editable=is_editable,
                    is_required=is_required,
                    is_searchable=is_searchable,
                    is_sortable=is_sortable,
                    is_filterable=is_filterable,
                    display_order=display_order,
                    min_length=min_length,
                    max_length=max_length,
                    min_value=min_value,
                    max_value=max_value,
                    validation_rules=validation_rules,
                    display_settings=display_settings,
                    help_text=help_text,
                    id_metadata_object=metadata_object.id
                )
                db_session.add(metadata_field)
                display_order += 1
                total_fields += 1
            
            # Clear the progress line and show summary for this model
            if model_fields_with_metadata > 0:
                ProgressDisplay.finalize_line(f"  Created {display_order} fields for {class_name} ({model_fields_with_metadata} with metadata)")
            else:
                print(f"  Created {display_order} fields for {class_name}")
        
        # Final summary
        if fields_with_metadata > 0:
            print(f"  Found metadata for {fields_with_metadata} fields across all models")
        
        print(f"Total fields created: {total_fields}")
        
        # Create metadata relationships based on foreign keys
        print(f"\nProcessing relationships...")
        total_relationships = 0
        
        for model_class in non_metadata_models:
            if not hasattr(model_class, '__tablename__'):
                continue
                
            class_name = model_class.__name__
            metadata_object = metadata_objects.get(class_name)
            if not metadata_object:
                continue
            
            # Get foreign key relationships
            try:
                inspector = sa_inspect(engine)
                table_name = model_class.__tablename__
                foreign_keys = inspector.get_foreign_keys(table_name)
            except Exception as e:
                print(f"Warning: Could not inspect foreign keys for table {table_name}: {e}")
                continue
            
            for fk in foreign_keys:
                # Find the target table name
                target_table = fk['referred_table']
                
                # Find the target model class
                target_model_class = None
                for other_model in non_metadata_models:
                    if hasattr(other_model, '__tablename__') and other_model.__tablename__ == target_table:
                        target_model_class = other_model
                        break
                
                if target_model_class:
                    target_class_name = target_model_class.__name__
                    target_metadata_object = metadata_objects.get(target_class_name)
                    
                    if target_metadata_object:
                        # Create relationship name
                        relationship_name = f"{class_name.lower()}_{target_class_name.lower()}"
                        display_name = f"{metadata_object.name} to {target_metadata_object.name}"
                        
                        # Determine relationship type (simplified - could be enhanced)
                        relationship_type = 'many_to_one'  # Default assumption
                        
                        # Create metadata relationship
                        metadata_relationship = MetadataRelationship(
                            name=relationship_name,
                            display_name=display_name,
                            description=f"Relationship between {class_name} and {target_class_name}",
                            relationship_type=relationship_type,
                            source_object_type=class_name,
                            target_object_type=target_class_name,
                            id_metadata_object_source=metadata_object.id,
                            id_metadata_object_target=target_metadata_object.id
                        )
                        db_session.add(metadata_relationship)
                        total_relationships += 1
        
        print(f"Total relationships created: {total_relationships}")
        
        # Commit all changes
        db_session.commit()
        print(f"\nPopulated metadata tables with {len(metadata_objects)} objects, {total_fields} fields, and {total_relationships} relationships")
    except Exception as e:
        print(f"Error: Could not populate metadata tables: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()




def load_stats_layouts():
    """Seed default stats layout ordering for key dashboards."""

    print('Loading stats layouts...')
    db_session = SessionLocal()
    try:
        user_id_row = db_session.query(User.id).order_by(User.id).first()
        if not user_id_row:
            print('No users found; skipping stats layout seed')
            return
        user_id = user_id_row[0]

        defaults = [
            {"id_user": user_id, "layout_key": 'buyers', "component_order": [
                'total_buyers',
                'total_purchase',
                'total_disputes',
                'total_orders',
            ]},
            {"id_user": user_id, "layout_key": 'sellers', "component_order": [
                'total_sellers',
                'total_listings',
                'total_disputes',
                'total_sales',
            ]},
        ]

        existing = {
            (layout.id_user, layout.layout_key)
            for layout in db_session.query(StatsLayout).filter(StatsLayout.id_user == user_id).all()
        }

        created = 0
        for row in defaults:
            key = (row['id_user'], row['layout_key'])
            if key in existing:
                continue
            layout = StatsLayout(**row)
            db_session.add(layout)
            created += 1

        if created:
            db_session.commit()
            print(f'Inserted {created} stats layouts for user {user_id}')
        else:
            print(f'Stats layouts already present for user {user_id}, skipping')
    finally:
        db_session.close()

def load_lead_delivery_trend_reports():
    column_mapping = {
        'Date': 'date',
        'Metric Type': 'metric_type',
        'Count': 'count',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/lead_delivery_trend_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping lead delivery trend reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping lead delivery trend reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading lead delivery trend reports", "reports")

            lead_delivery_trend_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'date':
                        try:
                            lead_delivery_trend_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            lead_delivery_trend_report_data[db_column] = None
                    # Handle count (integer)
                    elif db_column == 'count':
                        try:
                            lead_delivery_trend_report_data[db_column] = int(value)
                        except:
                            lead_delivery_trend_report_data[db_column] = 0
                    # Handle seller ID (nullable integer)
                    elif db_column == 'id_seller':
                        try:
                            lead_delivery_trend_report_data[db_column] = int(value) if value else None
                        except:
                            lead_delivery_trend_report_data[db_column] = None
                    # Handle metric type (convert to snake_case for constants)
                    elif db_column == 'metric_type':
                        # Convert display names to snake_case constants
                        metric_mapping = {
                            'Delivered': 'delivered',
                            'Accepted': 'accepted',
                            'Rejected': 'rejected',
                        }
                        lead_delivery_trend_report_data[db_column] = metric_mapping.get(value, str(value).lower().replace(' ', '_'))
                    else:
                        lead_delivery_trend_report_data[db_column] = value

            lead_delivery_trend_report = LeadDeliveryTrendReport(**lead_delivery_trend_report_data)
            db_session.add(lead_delivery_trend_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} lead delivery trend reports into the database")
    finally:
        db_session.close()


def load_top_categories_by_purchase_reports():
    column_mapping = {
        'Category': 'category',
        'Purchase Count': 'purchase_count',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/top_categories_by_purchase_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping top categories by purchase reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping top categories by purchase reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading top categories by purchase reports", "reports")

            top_categories_by_purchase_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle purchase count (integer)
                    if db_column == 'purchase_count':
                        try:
                            top_categories_by_purchase_report_data[db_column] = int(value)
                        except:
                            top_categories_by_purchase_report_data[db_column] = 0
                    # Handle seller ID (nullable integer)
                    elif db_column == 'id_seller':
                        try:
                            top_categories_by_purchase_report_data[db_column] = int(value) if value else None
                        except:
                            top_categories_by_purchase_report_data[db_column] = None
                    # Handle category (convert to snake_case for constants)
                    elif db_column == 'category':
                        # Convert display names to snake_case constants
                        category_mapping = {
                            'Energy & Utilities': 'energy_utilities',
                            'Advertising Data': 'advertising_data',
                            'Financial & Insurance': 'financial_insurance',
                            'Home Improvements': 'home_improvements',
                            'Residential Data': 'residential_data',
                        }
                        top_categories_by_purchase_report_data[db_column] = category_mapping.get(value, str(value).lower().replace(' ', '_').replace('&', '').replace('__', '_'))
                    else:
                        top_categories_by_purchase_report_data[db_column] = value

            top_categories_by_purchase_report = TopCategoriesByPurchaseReport(**top_categories_by_purchase_report_data)
            db_session.add(top_categories_by_purchase_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} top categories by purchase reports into the database")
    finally:
        db_session.close()


def load_dispute_insights_reports():
    column_mapping = {
        'Metric Type': 'metric_type',
        'Metric Category': 'metric_category',
        'Count': 'count',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/dispute_insights_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping dispute insights reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping dispute insights reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading dispute insights reports", "reports")

            dispute_insights_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle integer fields
                    if db_column == 'count':
                        try:
                            dispute_insights_report_data[db_column] = int(value)
                        except:
                            dispute_insights_report_data[db_column] = 0
                    # Handle seller ID (nullable)
                    elif db_column == 'id_seller':
                        try:
                            dispute_insights_report_data[db_column] = int(value) if value else None
                        except:
                            dispute_insights_report_data[db_column] = None
                    else:
                        dispute_insights_report_data[db_column] = value

            dispute_insights_report = DisputeInsightsReport(**dispute_insights_report_data)
            db_session.add(dispute_insights_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} dispute insights reports into the database")
    finally:
        db_session.close()


def load_top_dispute_reasons_reports():
    column_mapping = {
        'Reason': 'reason',
        'Purchase Count': 'purchase_count',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/top_dispute_reasons_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping top dispute reasons reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping top dispute reasons reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading top dispute reasons reports", "reports")

            top_dispute_reasons_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle integer fields
                    if db_column == 'purchase_count':
                        try:
                            top_dispute_reasons_report_data[db_column] = int(value)
                        except:
                            top_dispute_reasons_report_data[db_column] = 0
                    # Handle seller ID (nullable)
                    elif db_column == 'id_seller':
                        try:
                            top_dispute_reasons_report_data[db_column] = int(value) if value else None
                        except:
                            top_dispute_reasons_report_data[db_column] = None
                    else:
                        top_dispute_reasons_report_data[db_column] = value

            top_dispute_reasons_report = TopDisputeReasonsReport(**top_dispute_reasons_report_data)
            db_session.add(top_dispute_reasons_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} top dispute reasons reports into the database")
    finally:
        db_session.close()


def load_api_usage_reports():
    column_mapping = {
        'ID User': 'id_user',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Total API Calls': 'total_api_calls',
        'Successful Calls': 'successful_calls',
        'Failed Calls': 'failed_calls',
        'Success Rate(%)': 'success_rate',
        'Most Common Error': 'most_common_error',
        'Status': 'status',
    }

    csv_path = 'data/csv/api_usage_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping API usage reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping API usage reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading API usage reports", "reports")

            api_usage_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle integer fields
                    if db_column in ['total_api_calls', 'successful_calls', 'failed_calls']:
                        try:
                            api_usage_report_data[db_column] = int(value)
                        except:
                            api_usage_report_data[db_column] = 0
                    # Handle percentage field
                    elif db_column == 'success_rate':
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            api_usage_report_data[db_column] = float(clean_value)
                        except:
                            api_usage_report_data[db_column] = 0.00
                    else:
                        api_usage_report_data[db_column] = value

            api_usage_report = ApiUsageReport(**api_usage_report_data)
            db_session.add(api_usage_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} API usage reports into the database")
    finally:
        db_session.close()


def load_most_verified_reports():
    column_mapping = {
        'ID User': 'id_user',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Total Checks': 'total_checks',
        'DD Checks': 'dd_checks',
        'KYC Checks': 'kyc_checks',
        'DD & KYC Checks': 'dd_kyc_checks',
        'Spent On Credits': 'spent_on_credits',
        'Last Check': 'last_check',
        'Status': 'status',
    }

    csv_path = 'data/csv/most_verified_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping most verified reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping most verified reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading most verified reports", "reports")

            most_verified_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'last_check':
                        try:
                            most_verified_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            most_verified_report_data[db_column] = None
                    # Handle integer check fields
                    elif db_column in ['total_checks', 'dd_checks', 'kyc_checks', 'dd_kyc_checks']:
                        try:
                            most_verified_report_data[db_column] = int(value)
                        except:
                            most_verified_report_data[db_column] = 0
                    # Handle currency field
                    elif db_column == 'spent_on_credits':
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            most_verified_report_data[db_column] = float(clean_value)
                        except:
                            most_verified_report_data[db_column] = 0.00
                    else:
                        most_verified_report_data[db_column] = value

            most_verified_report = MostVerifiedReport(**most_verified_report_data)
            db_session.add(most_verified_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} most verified reports into the database")
    finally:
        db_session.close()


def load_credit_purchased_reports():
    column_mapping = {
        'ID User': 'id_user',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Credit Purchased': 'credit_purchased',
        'Credit Used': 'credit_used',
        'Remaining Credits': 'remaining_credits',
        'Spent On Credits': 'spent_on_credits',
        'Last Top Up': 'last_top_up',
        'Status': 'status',
    }

    csv_path = 'data/csv/credit_purchased_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping credit purchased reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping credit purchased reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading credit purchased reports", "reports")

            credit_purchased_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'last_top_up':
                        try:
                            credit_purchased_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            credit_purchased_report_data[db_column] = None
                    # Handle integer credit fields
                    elif db_column in ['credit_purchased', 'credit_used', 'remaining_credits']:
                        try:
                            credit_purchased_report_data[db_column] = int(value)
                        except:
                            credit_purchased_report_data[db_column] = 0
                    # Handle currency field
                    elif db_column == 'spent_on_credits':
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            credit_purchased_report_data[db_column] = float(clean_value)
                        except:
                            credit_purchased_report_data[db_column] = 0.00
                    else:
                        credit_purchased_report_data[db_column] = value

            credit_purchased_report = CreditPurchasedReport(**credit_purchased_report_data)
            db_session.add(credit_purchased_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} credit purchased reports into the database")
    finally:
        db_session.close()


def calculate_permission_bit_sequence_from_csv(permissions_str):
    """
    Calculate the permission bit sequence from permissions string.

    Example:
        "1,2,3" -> "7"
        "1-3" -> "7"
        "1,2,3,4-6" -> "127"
    """

    if not permissions_str or pd.isna(permissions_str):
        return "0"
    
    # Initialize result to 0
    result = 0
    
    # Split by comma and process each segment
    segments = [s.strip() for s in permissions_str.split(',')]
    for segment in segments:
        if '-' in segment:
            # Handle range (e.g., "1-3")
            start, end = map(int, segment.split('-'))
            for num in range(start, end + 1):
                result |= (2 ** (num - 1))
        else:
            # Handle single number
            num = int(segment)
            result |= (2 ** (num - 1))
    
    return str(result)


def export_sheets_to_csv():
    """Export Excel sheets to CSV files"""

    excel_files = [
        'data/tds_admin_base_data.xlsx',
    ]
    csv_dir = 'data/csv'
    
    # Ensure CSV directory exists
    os.makedirs(csv_dir, exist_ok=True)
    
    # Count total sheets for progress tracking
    total_sheets = 0
    all_sheets = []
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            xlsx = pd.ExcelFile(excel_file)
            for sheet_name in xlsx.sheet_names:
                all_sheets.append((excel_file, sheet_name))
                total_sheets += 1
    
    print(f"Exporting {total_sheets} sheets to CSV...")
    
    # Process all sheets with progress
    for index, (excel_file, sheet_name) in enumerate(all_sheets):
        ProgressDisplay.show_progress(index + 1, total_sheets, "Exporting Excel sheets", "sheets")
        
        # Read the sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Generate CSV filename using snake case
        csv_filename = f"{to_snake_case(sheet_name)}.csv"
        csv_path = os.path.join(csv_dir, csv_filename)
        
        # Export to CSV
        df.to_csv(csv_path, index=False)
    
    ProgressDisplay.finalize_line(f"Exported {total_sheets} Excel sheets to CSV files")


def load_users():
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Password': 'password',
        'Status': 'status',
        'Role': 'id_role',
    }

    csv_files = [
        'data/csv/users.csv',
        'data/csv/test_users.csv',
    ]

    dfs = []
    for csv_path in csv_files:
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                dfs.append(df)
            except Exception:
                print(f"Warning: Failed to read {csv_path}, skipping...")
        else:
            print(f"Info: {csv_path} not found, skipping...")

    if not dfs:
        print("Info: No user CSV files found, skipping user load")
        return

    df = pd.concat(dfs, ignore_index=True)

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading users", "users")

            user_data = {
                db_column: row.get(csv_column)
                for csv_column, db_column in column_mapping.items()
            }

            try:
                user_data['password'] = bcrypt.hashpw(
                    str(user_data.get('password') or '').encode('utf-8'),
                    bcrypt.gensalt(),
                ).decode('utf-8')
            except Exception:
                user_data['password'] = bcrypt.hashpw(
                    b'default-password', bcrypt.gensalt()
                ).decode('utf-8')

            user = User(**user_data)
            db_session.add(user)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} users into the database")
    finally:
        db_session.close()


def load_roles():
    column_mapping = {
        'Name': 'name',
    }

    csv_path = 'data/csv/roles.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping global roles load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping global roles load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading global roles", "roles")

            role_data = {
                db_column: row.get(csv_column)
                for csv_column, db_column in column_mapping.items()
            }

            role_data['permission_bit_sequence'] = calculate_permission_bit_sequence_from_csv(
                row.get('Permissions', ''),
            )

            role = Role(**role_data)
            db_session.add(role)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} global roles into the database")
    finally:
        db_session.close()


def load_event_types():
    column_mapping = {
        'Token': 'token',
        'Name': 'name',
        'Message': 'message',
        'Notes': 'notes',
    }

    csv_path = 'data/csv/event_types.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping event types load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping event types load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading event types", "types")

            event_type_data = {
                db_column: (row.get(csv_column) if pd.notna(row.get(csv_column)) else None)
                for csv_column, db_column in column_mapping.items()
            }

            event_type = EventType(**event_type_data)
            db_session.add(event_type)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} event types into the database")
    finally:
        db_session.close()


def load_data_types():
    column_mapping = {
        'Name': 'name',
        'Description': 'description',
        'Status': 'status',
    }

    csv_path = 'data/csv/data_types.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping data types load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping data types load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading data types", "types")

            data_type_data = {
                db_column: (row.get(csv_column) if pd.notna(row.get(csv_column)) else None)
                for csv_column, db_column in column_mapping.items()
            }

            data_type = DataType(**data_type_data)
            db_session.add(data_type)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} data types into the database")
    finally:
        db_session.close()


def load_categories():
    column_mapping = {
        'Category Name': 'name',
        'Data Type': 'data_type_name',  # We'll resolve this to id_data_type
        'Status': 'status',
        'Icon ID': 'id_icon',
    }

    csv_path = 'data/csv/categories.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping categories load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping categories load")
        return

    db_session = SessionLocal()
    try:
        # Get data types for lookup
        data_types = {dt.name: dt.id for dt in db_session.query(DataType).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading categories", "categories")

            # Map basic fields
            category_data = {}
            for csv_column, db_column in column_mapping.items():
                if csv_column != 'Data Type':  # Handle data type separately
                    value = row.get(csv_column)
                    if pd.notna(value):
                        category_data[db_column] = value

            # Resolve data type name to ID
            data_type_name = row.get('Data Type')
            if pd.notna(data_type_name) and data_type_name in data_types:
                category_data['id_data_type'] = data_types[data_type_name]
            else:
                print(f"Warning: Data type '{data_type_name}' not found, skipping category")
                continue

            # Remove the temporary field
            category_data.pop('data_type_name', None)

            category = Category(**category_data)
            db_session.add(category)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} categories into the database")
    finally:
        db_session.close()


def load_sub_categories():
    column_mapping = {
        'Sub Category Name': 'name',
        'Category Name': 'category_name',  # We'll resolve this to id_category
        'Data Type': 'data_type_name',  # We'll resolve this to id_data_type
        'Status': 'status',
        'Icon ID': 'id_icon',
    }

    csv_path = 'data/csv/sub_categories.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping sub categories load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping sub categories load")
        return

    db_session = SessionLocal()
    try:
        # Get data types and categories for lookup
        data_types = {dt.name: dt.id for dt in db_session.query(DataType).all()}
        categories = {cat.name: cat.id for cat in db_session.query(Category).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading sub categories", "sub categories")

            # Map basic fields
            sub_category_data = {}
            for csv_column, db_column in column_mapping.items():
                if csv_column not in ['Category Name', 'Data Type']:  # Handle lookups separately
                    value = row.get(csv_column)
                    if pd.notna(value):
                        sub_category_data[db_column] = value

            # Resolve category name to ID
            category_name = row.get('Category Name')
            if pd.notna(category_name) and category_name in categories:
                sub_category_data['id_category'] = categories[category_name]
            else:
                print(f"Warning: Category '{category_name}' not found, skipping sub category")
                continue

            # Resolve data type name to ID
            data_type_name = row.get('Data Type')
            if pd.notna(data_type_name) and data_type_name in data_types:
                sub_category_data['id_data_type'] = data_types[data_type_name]
            else:
                print(f"Warning: Data type '{data_type_name}' not found, skipping sub category")
                continue

            # Remove the temporary fields
            sub_category_data.pop('category_name', None)
            sub_category_data.pop('data_type_name', None)

            sub_category = SubCategory(**sub_category_data)
            db_session.add(sub_category)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} sub categories into the database")
    finally:
        db_session.close()


def load_selections():
    column_mapping = {
        'Selection Name': 'name',
        'Sub Category Name': 'sub_category_name',  # We'll resolve this to id_sub_category
        'Category Name': 'category_name',  # We'll resolve this to id_category
        'Data Type': 'data_type_name',  # We'll resolve this to id_data_type
        'Selection ID': 'selection_id',
        'Status': 'status',
        'Icon ID': 'id_icon',
    }

    csv_path = 'data/csv/selections.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping selections load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping selections load")
        return

    db_session = SessionLocal()
    try:
        # Get data types, categories, and sub categories for lookup
        data_types = {dt.name: dt.id for dt in db_session.query(DataType).all()}
        categories = {cat.name: cat.id for cat in db_session.query(Category).all()}
        sub_categories = {sub_cat.name: sub_cat.id for sub_cat in db_session.query(SubCategory).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading selections", "selections")

            # Map basic fields
            selection_data = {}
            for csv_column, db_column in column_mapping.items():
                if csv_column not in ['Sub Category Name', 'Category Name', 'Data Type']:  # Handle lookups separately
                    value = row.get(csv_column)
                    if pd.notna(value):
                        selection_data[db_column] = value

            # Resolve sub category name to ID
            sub_category_name = row.get('Sub Category Name')
            if pd.notna(sub_category_name) and sub_category_name in sub_categories:
                selection_data['id_sub_category'] = sub_categories[sub_category_name]
            else:
                print(f"Warning: Sub category '{sub_category_name}' not found, skipping selection")
                continue

            # Resolve category name to ID
            category_name = row.get('Category Name')
            if pd.notna(category_name) and category_name in categories:
                selection_data['id_category'] = categories[category_name]
            else:
                print(f"Warning: Category '{category_name}' not found, skipping selection")
                continue

            # Resolve data type name to ID
            data_type_name = row.get('Data Type')
            if pd.notna(data_type_name) and data_type_name in data_types:
                selection_data['id_data_type'] = data_types[data_type_name]
            else:
                print(f"Warning: Data type '{data_type_name}' not found, skipping selection")
                continue

            # Remove the temporary fields
            selection_data.pop('sub_category_name', None)
            selection_data.pop('category_name', None)
            selection_data.pop('data_type_name', None)

            selection = Selection(**selection_data)
            db_session.add(selection)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} selections into the database")
    finally:
        db_session.close()


def load_activity_logs():
    column_mapping = {
        'Activity Type': 'activity_type',
        'Activity Category': 'activity_category',
        'Title': 'title',
        'Description': 'description',
        'User ID': 'id_user',
        'Company ID': 'id_company',
        'Order ID': 'id_order',
        'Dispute ID': 'id_dispute',
        'Product ID': 'id_product',
        'DD User ID': 'id_dd_user',
        'Metadata': 'activity_metadata',
    }

    csv_path = 'data/csv/activity_logs.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping activity logs load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping activity logs load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading activity logs", "logs")

            activity_log_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column in ['id_user', 'id_company', 'id_order', 'id_dispute', 'id_product', 'id_dd_user']:
                        try:
                            activity_log_data[db_column] = int(value)
                        except Exception:
                            activity_log_data[db_column] = None
                    elif db_column == 'activity_metadata' and isinstance(value, str):
                        try:
                            activity_log_data[db_column] = json.loads(value)
                        except json.JSONDecodeError:
                            activity_log_data[db_column] = None
                    else:
                        activity_log_data[db_column] = value

            activity_log = ActivityLog(**activity_log_data)
            db_session.add(activity_log)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} activity logs into the database")
    finally:
        db_session.close()


def load_transactions():
    column_mapping = {
        'Transaction ID': 'id_transaction',
        'Order ID': 'id_order',
        'Transaction Date': 'transaction_date',
        'Sale Price': 'sale_price',
        'VAT Amount': 'vat_amount',
        'TDS Fee': 'tds_fee',
        'Payment Provider Fee': 'payment_provider_fee',
        'Net Payable': 'net_payable',
        'Remaining VAT': 'remaining_vat',
        'Total Payable': 'total_payable',
        'Payable Date': 'payable_date',
        'Status': 'status',
        'Portal': 'portal',
        'Invoice ID': 'invoice_id',
        'Invoice URL': 'invoice_url',
        'Payment Provider': 'payment_provider',
        'Notes': 'notes',
        'Buyer ID': 'id_buyer',
        'Seller ID': 'id_seller',
        'Product ID': 'id_product',
    }

    csv_path = 'data/csv/transactions.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping transactions load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping transactions load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading transactions", "transactions")

            transaction_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column in ['transaction_date']:
                        try:
                            transaction_data[db_column] = pd.to_datetime(value)
                        except:
                            transaction_data[db_column] = None
                    elif db_column in ['payable_date']:
                        try:
                            transaction_data[db_column] = pd.to_datetime(value).date()
                        except:
                            transaction_data[db_column] = None
                    elif db_column in ['id_buyer', 'id_seller', 'id_product']:
                        try:
                            transaction_data[db_column] = int(value)
                        except:
                            transaction_data[db_column] = None
                    elif db_column in ['sale_price', 'vat_amount', 'tds_fee', 'payment_provider_fee', 'net_payable', 'remaining_vat', 'total_payable']:
                        try:
                            transaction_data[db_column] = float(value)
                        except:
                            transaction_data[db_column] = None
                    else:
                        transaction_data[db_column] = str(value).strip() if isinstance(value, str) else value

            transaction = Transaction(**transaction_data)
            db_session.add(transaction)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} transactions into the database")
    finally:
        db_session.close()


def load_blogs():
    column_mapping = {
        'Title': 'title',
        'Category ID': 'id_category',
        'Publication Status': 'publication_status',
        'Blog Status': 'blog_status',
        'User ID': 'id_user',
    }

    csv_path = 'data/csv/blogs.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping blogs load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping blogs load")
        return

    df = df.reset_index(drop=True)

    valid_publication_statuses = {'PUBLISHED', 'PENDING'}
    valid_blog_statuses = {'ACTIVE', 'ARCHIVED'}

    db_session = SessionLocal()
    try:
        category_ids = {category.id for category in db_session.query(Category).all()}
        user_ids = {user.id for user in db_session.query(User).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading blogs", "blogs")

            blog_data = {}
            skip_record = False

            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.isna(value):
                    continue

                if db_column in ['id_category', 'id_user']:
                    try:
                        blog_data[db_column] = int(value)
                    except Exception:
                        blog_data[db_column] = None
                elif db_column in ['publication_status', 'blog_status']:
                    normalized_value = str(value).strip().upper()
                    if db_column == 'publication_status' and normalized_value not in valid_publication_statuses:
                        print(f"Warning: Invalid publication status '{value}', skipping blog")
                        skip_record = True
                        break
                    if db_column == 'blog_status' and normalized_value not in valid_blog_statuses:
                        print(f"Warning: Invalid blog status '{value}', skipping blog")
                        skip_record = True
                        break
                    blog_data[db_column] = normalized_value
                else:
                    blog_data[db_column] = str(value).strip()

            if skip_record:
                continue

            category_id = blog_data.get('id_category')
            if category_id is not None and category_id not in category_ids:
                print(f"Warning: Category ID {category_id} not found, skipping blog")
                continue

            user_id = blog_data.get('id_user')
            if user_id is not None and user_id not in user_ids:
                print(f"Warning: User ID {user_id} not found, skipping blog")
                continue

            blog = Blog(**blog_data)
            db_session.add(blog)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} blogs into the database")
    finally:
        db_session.close()


def load_orders():
    column_mapping = {
        'Title': 'title',
        'Description': 'description',
        'Order Date': 'order_date',
        'Completion Date': 'completion_date',
        'Product ID': 'id_product',
        'Quantity Ordered': 'quantity_ordered',
        'Unit Price': 'unit_price',
        'Total Amount': 'total_amount',
        'Discount Amount': 'discount_amount',
        'Final Amount': 'final_amount',
        'Status': 'status',
        'Payment Status': 'payment_status',
        'Delivery Status': 'delivery_status',
        'Buyer ID': 'id_buyer',
        'Company ID': 'id_company',
    }

    csv_path = 'data/csv/orders.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping orders load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping orders load")
        return

    db_session = SessionLocal()
    try:
        # Get related entities for validation
        product_ids = {prod.id for prod in db_session.query(Product).all()}
        company_ids = {comp.id for comp in db_session.query(Company).all()}
        buyer_ids = {buyer.id for buyer in db_session.query(Buyer).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading orders", "orders")

            order_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column in ['order_date', 'completion_date']:
                        try:
                            order_data[db_column] = pd.to_datetime(value)
                        except Exception:
                            order_data[db_column] = None
                    # Handle numeric fields
                    elif db_column in ['quantity_ordered']:
                        try:
                            order_data[db_column] = int(value)
                        except Exception:
                            order_data[db_column] = 1
                    elif db_column in ['unit_price', 'total_amount', 'discount_amount', 'final_amount']:
                        try:
                            order_data[db_column] = float(value)
                        except Exception:
                            order_data[db_column] = None
                    elif db_column in ['id_product', 'id_buyer', 'id_company']:
                        try:
                            order_data[db_column] = int(value)
                        except Exception:
                            order_data[db_column] = None
                    else:
                        order_data[db_column] = value

            # Validate required foreign key relationships
            validation_checks = [
                ('id_product', product_ids, 'Product'),
                ('id_buyer', buyer_ids, 'Buyer'),
                ('id_company', company_ids, 'Company'),
            ]

            skip_record = False
            for field_name, valid_ids, entity_name in validation_checks:
                entity_id = order_data.get(field_name)
                if entity_id is None:
                    print(f"Warning: No {entity_name} ID provided, skipping order")
                    skip_record = True
                    break
                if valid_ids and entity_id not in valid_ids:
                    print(f"Warning: {entity_name} ID {entity_id} not found, skipping order")
                    skip_record = True
                    break

            if skip_record:
                continue

            order = Order(**order_data)
            db_session.add(order)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} orders into the database")
    finally:
        db_session.close()


def load_dataset_orders():
    csv_path = 'data/csv/dataset_orders.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping dataset orders load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping dataset orders load")
        return

    db_session = SessionLocal()
    try:
        product_map = {product.name: product.id for product in db_session.query(Product).all()}
        company_map = {company.name: company.id for company in db_session.query(Company).all()}

        def parse_bool(value, default=False):
            if pd.isna(value):
                return default
            normalized = str(value).strip().lower()
            if normalized in ['true', '1', 'yes', 'y']:
                return True
            if normalized in ['false', '0', 'no', 'n']:
                return False
            return default

        created = 0
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading dataset orders", "dataset_orders")

            order_code = row.get('Order Code')
            if pd.isna(order_code):
                print('Warning: Order Code missing, skipping dataset order row')
                continue
            order_code = str(order_code).strip()
            if not order_code:
                print('Warning: Blank Order Code encountered, skipping dataset order row')
                continue

            existing = (
                db_session.query(DatasetOrder)
                .filter(DatasetOrder.order_code == order_code)
                .first()
            )
            if existing:
                continue

            product_name = row.get('Product Name')
            product_id = product_map.get(str(product_name).strip()) if pd.notna(product_name) else None
            if not product_id:
                print(f"Warning: Product '{product_name}' not found, skipping dataset order {order_code}")
                continue

            buyer_name = row.get('Buyer Company')
            buyer_company_id = company_map.get(str(buyer_name).strip()) if pd.notna(buyer_name) else None
            if not buyer_company_id:
                print(f"Warning: Buyer company '{buyer_name}' not found, skipping dataset order {order_code}")
                continue

            seller_name = row.get('Seller Company')
            seller_company_id = company_map.get(str(seller_name).strip()) if pd.notna(seller_name) else None
            if not seller_company_id:
                print(f"Warning: Seller company '{seller_name}' not found, skipping dataset order {order_code}")
                continue

            ordered_on_raw = row.get('Ordered On')
            ordered_on = None
            if pd.notna(ordered_on_raw):
                try:
                    ordered_on = pd.to_datetime(ordered_on_raw, utc=True, errors='coerce')
                except Exception:
                    ordered_on = None
            if ordered_on is None or pd.isna(ordered_on):
                print(f"Warning: Ordered On missing for {order_code}, skipping")
                continue

            licence_expires_raw = row.get('Licence Expires On')
            licence_expires_on = None
            if pd.notna(licence_expires_raw):
                parsed_date = pd.to_datetime(licence_expires_raw, errors='coerce')
                if not pd.isna(parsed_date):
                    licence_expires_on = parsed_date.date()

            def parse_int(value, default=None):
                if pd.isna(value):
                    return default
                try:
                    return int(value)
                except Exception:
                    return default

            def parse_float(value, default=None):
                if pd.isna(value):
                    return default
                try:
                    return float(value)
                except Exception:
                    return default

            status_value = str(row.get('Status', '')).strip().lower()
            if status_value not in DatasetOrderStatus._value2member_map_:
                status_value = DatasetOrderStatus.ACCEPTED.value

            licence_status_value = str(row.get('Licence Status', '')).strip().lower()
            if licence_status_value not in DatasetLicenceStatus._value2member_map_:
                licence_status_value = DatasetLicenceStatus.ACTIVE.value

            dispute_status_value = str(row.get('Dispute Status', '')).strip().lower()
            if dispute_status_value not in DatasetDisputeStatus._value2member_map_:
                dispute_status_value = DatasetDisputeStatus.NONE.value

            refund_status_value = str(row.get('Refund Status', '')).strip().lower()
            if refund_status_value not in DatasetRefundStatus._value2member_map_:
                refund_status_value = DatasetRefundStatus.NONE.value

            forwarding_status_value = str(row.get('Forwarding Status', '')).strip().lower()
            if forwarding_status_value not in DatasetForwardingStatus._value2member_map_:
                forwarding_status_value = DatasetForwardingStatus.SUCCESS.value

            query_rules_raw = row.get('Query Rules')
            query_rules = None
            if pd.notna(query_rules_raw) and str(query_rules_raw).strip():
                try:
                    query_rules = json.loads(query_rules_raw)
                except json.JSONDecodeError:
                    print(f"Warning: Invalid Query Rules JSON for {order_code}, storing as None")
                    query_rules = None

            dataset_order_data = {
                'order_code': order_code,
                'id_product': product_id,
                'id_buyer_company': buyer_company_id,
                'id_seller_company': seller_company_id,
                'ordered_on': ordered_on.to_pydatetime(),
                'quantity': parse_int(row.get('Quantity'), 0),
                'unit_price': parse_float(row.get('Unit Price'), 0.0),
                'total_value': parse_float(row.get('Total Value'), 0.0),
                'currency': str(row.get('Currency', 'GBP')).strip()[:3] or 'GBP',
                'dupecheck_passed': parse_bool(row.get('DupeCheck Passed'), True),
                'tps_match_count': parse_int(row.get('TPS Match Count'), 0),
                'status': status_value,
                'licence_status': licence_status_value,
                'licence_expires_on': licence_expires_on,
                'dispute_status': dispute_status_value,
                'dispute_count': parse_int(row.get('Dispute Count'), 0),
                'dispute_summary': None if pd.isna(row.get('Dispute Summary')) else str(row.get('Dispute Summary')).strip(),
                'refund_status': refund_status_value,
                'refund_value': parse_float(row.get('Refund Value')),
                'coverage_enabled': parse_bool(row.get('Coverage Enabled'), True),
                'advanced_filters_enabled': parse_bool(row.get('Advanced Filters Enabled'), False),
                'query_count': parse_int(row.get('Query Count')),
                'query_rules': query_rules,
                'forwarding_status': forwarding_status_value,
                'retry_count_total': parse_int(row.get('Retry Count Total'), 0),
                'notes': None if pd.isna(row.get('Notes')) else str(row.get('Notes')).strip(),
            }

            dataset_order = DatasetOrder(**dataset_order_data)
            db_session.add(dataset_order)
            created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} dataset orders into the database")
    finally:
        db_session.close()


def load_dataset_order_deliveries():
    csv_path = 'data/csv/dataset_order_deliveries.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping dataset order deliveries load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping dataset order deliveries load")
        return

    db_session = SessionLocal()
    try:
        order_map = {order.order_code: order.id for order in db_session.query(DatasetOrder).all()}

        def parse_bool(value, default=False):
            if pd.isna(value):
                return default
            normalized = str(value).strip().lower()
            if normalized in ['true', '1', 'yes', 'y']:
                return True
            if normalized in ['false', '0', 'no', 'n']:
                return False
            return default

        created = 0
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading dataset order deliveries", "dataset_order_deliveries")

            delivery_code = row.get('Delivery Code')
            if pd.isna(delivery_code):
                print('Warning: Delivery Code missing, skipping delivery row')
                continue
            delivery_code = str(delivery_code).strip()
            if not delivery_code:
                print('Warning: Blank Delivery Code encountered, skipping delivery row')
                continue

            existing = (
                db_session.query(DatasetOrderDelivery)
                .filter(DatasetOrderDelivery.delivery_code == delivery_code)
                .first()
            )
            if existing:
                continue

            order_code = row.get('Order Code')
            dataset_order_id = order_map.get(str(order_code).strip()) if pd.notna(order_code) else None
            if not dataset_order_id:
                print(f"Warning: Dataset order with code '{order_code}' not found, skipping delivery {delivery_code}")
                continue

            delivered_on_raw = row.get('Delivered On')
            delivered_on = None
            if pd.notna(delivered_on_raw):
                try:
                    delivered_on = pd.to_datetime(delivered_on_raw, utc=True, errors='coerce')
                except Exception:
                    delivered_on = None
            if delivered_on is None or pd.isna(delivered_on):
                print(f"Warning: Delivered On missing for delivery {delivery_code}, skipping")
                continue

            hlr_result = str(row.get('HLR Result', '')).strip().lower()
            if hlr_result not in ['yes', 'no', 'n/a']:
                hlr_result = 'yes'

            llv_result = str(row.get('LLV Result', '')).strip().lower()
            if llv_result not in ['yes', 'no', 'n/a']:
                llv_result = 'yes'

            status_value = str(row.get('Status', '')).strip().lower()
            if status_value not in DatasetDeliveryStatus._value2member_map_:
                status_value = DatasetDeliveryStatus.ACCEPTED.value

            forwarding_status_value = str(row.get('Forwarding Status', '')).strip().lower()
            if forwarding_status_value not in DatasetForwardingStatus._value2member_map_:
                forwarding_status_value = DatasetForwardingStatus.SUCCESS.value

            def parse_int(value, default=None):
                if pd.isna(value):
                    return default
                try:
                    return int(value)
                except Exception:
                    return default

            dataset_delivery_data = {
                'id_dataset_order': dataset_order_id,
                'delivery_code': delivery_code,
                'delivered_on': delivered_on.to_pydatetime(),
                'hlr_result': hlr_result,
                'llv_result': llv_result,
                'criteria_met': parse_bool(row.get('Criteria Met'), True),
                'status': status_value,
                'retry_count': parse_int(row.get('Retry Count'), 0),
                'dispute_reason': None if pd.isna(row.get('Dispute Reason')) else str(row.get('Dispute Reason')).strip(),
                'api_code': parse_int(row.get('API Code')),
                'forwarding_status': forwarding_status_value,
                'forwarding_notes': None if pd.isna(row.get('Forwarding Notes')) else str(row.get('Forwarding Notes')).strip(),
            }

            dataset_delivery = DatasetOrderDelivery(**dataset_delivery_data)
            db_session.add(dataset_delivery)
            created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} dataset order deliveries into the database")
    finally:
        db_session.close()


def load_live_lead_orders():
    """Seed representative live lead orders for mock API scenarios."""

    db_session = SessionLocal()
    try:
        if db_session.query(LiveLeadOrder).count():
            print('Live lead orders already exist; skipping live lead order seed')
            return

        product_ids = [
            row[0] for row in db_session.query(Product.id).order_by(Product.id).all()
        ]
        user_ids = [
            row[0] for row in db_session.query(User.id).order_by(User.id).all()
        ]

        if not product_ids:
            print('No products available; skipping live lead order seed')
            return
        if len(user_ids) < 2:
            print('Need at least two users to map buyer/seller; skipping live lead order seed')
            return

        now = datetime.utcnow()
        today = now.date()
        status_configs = [
            {
                'label': 'Pending Solar',
                'code_prefix': 'LLP',
                'status': LiveLeadOrderStatus.AWAITING_START_DATE.value,
                'connection_status': LiveLeadConnectionStatus.BUYER_NOT_CONNECTED.value,
                'api_connected': False,
                'api_url': 'https://buyer-pending.example/api/live',
                'leads_ratio': 0.0,
                'start_mode': 'future',
                'start_offset': 5,
                'end_mode': None,
            },
            {
                'label': 'Ongoing Finance',
                'code_prefix': 'LLO',
                'status': LiveLeadOrderStatus.ONGOING.value,
                'connection_status': LiveLeadConnectionStatus.BUYER_SELLER_CONNECTED.value,
                'api_connected': True,
                'api_url': 'https://buyer-ongoing.example/api/live',
                'leads_ratio': 0.55,
                'start_mode': 'past',
                'start_offset': 3,
                'end_mode': 'future',
                'end_offset': 20,
            },
            {
                'label': 'Completed Insurance',
                'code_prefix': 'LLC',
                'status': LiveLeadOrderStatus.COMPLETED.value,
                'connection_status': LiveLeadConnectionStatus.BUYER_SELLER_CONNECTED.value,
                'api_connected': True,
                'api_url': 'https://buyer-complete.example/api/live',
                'leads_ratio': 1.0,
                'start_mode': 'past',
                'start_offset': 2,
                'end_mode': 'after_start',
                'end_offset': 30,
            },
            {
                'label': 'Disputed Debt Relief',
                'code_prefix': 'LLD',
                'status': LiveLeadOrderStatus.DISPUTED.value,
                'connection_status': LiveLeadConnectionStatus.BUYER_SELLER_CONNECTED.value,
                'api_connected': True,
                'api_url': 'https://buyer-dispute.example/api/live',
                'leads_ratio': 0.4,
                'start_mode': 'past',
                'start_offset': 4,
                'end_mode': 'future',
                'end_offset': 10,
            },
        ]

        def compute_start_date(config, ordered_on, idx):
            mode = config.get('start_mode')
            offset = config.get('start_offset', 0)
            if mode == 'future':
                return today + timedelta(days=offset + idx)
            if mode == 'past':
                return ordered_on + timedelta(days=offset)
            return None

        def compute_end_date(config, ordered_on, start_date):
            mode = config.get('end_mode')
            offset = config.get('end_offset', 0)
            if mode == 'future':
                return today + timedelta(days=offset)
            if mode == 'after_start' and start_date:
                return start_date + timedelta(days=offset)
            if mode == 'past':
                return ordered_on + timedelta(days=offset)
            return None

        created = 0
        for config in status_configs:
            for idx in range(15):
                order_code = f'{config["code_prefix"]}{idx+1:04d}'
                ordered_on = today - timedelta(days=(idx * 2 + 10))
                leads_ordered = 600 + (idx * 25)
                start_date = compute_start_date(config, ordered_on, idx)
                end_date = compute_end_date(config, ordered_on, start_date)
                leads_delivered = int(leads_ordered * config['leads_ratio'])
                order_data = {
                    'order_code': order_code,
                    'product_id': product_ids[(idx + created) % len(product_ids)],
                    'buyer_id': user_ids[(idx + created) % len(user_ids)],
                    'seller_id': user_ids[(idx + created + 1) % len(user_ids)],
                    'ordered_on': ordered_on,
                    'leads_ordered': leads_ordered,
                    'leads_delivered': leads_delivered,
                    'connection_status': config['connection_status'],
                    'criteria': f'{config["label"]} cohort #{idx+1}',
                    'api_endpoint_url': config['api_url'],
                    'api_auth_key': f'{config["code_prefix"].lower()}-key-{idx+1:04d}',
                    'api_fields': ['first_name', 'last_name', 'email', 'mobile', 'zip_code'],
                    'api_is_connected': config['api_connected'],
                    'api_last_checked_at': now - timedelta(days=(idx % 5 + 1)),
                    'status': config['status'],
                    'start_date': start_date,
                    'end_date': end_date,
                }

                order = LiveLeadOrder(**order_data)
                db_session.add(order)
                created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} live lead orders into the database")
    finally:
        db_session.close()


def load_live_lead_delivery_schedules():
    """Create recurring delivery slots for seeded live lead orders."""

    db_session = SessionLocal()
    try:
        if db_session.query(LiveLeadDeliverySchedule).count():
            print('Live lead delivery schedules already exist; skipping schedule seed')
            return

        orders = db_session.query(LiveLeadOrder).all()
        if not orders:
            print('No live lead orders available; skipping delivery schedule seed')
            return

        status_based_templates = {
            LiveLeadOrderStatus.AWAITING_START_DATE.value: [
                {'day': LiveLeadDeliveryDay.MONDAY.value, 'start': time_of_day(9, 0), 'end': time_of_day(12, 0), 'capacity': 150},
                {'day': LiveLeadDeliveryDay.WEDNESDAY.value, 'start': time_of_day(13, 0), 'end': time_of_day(17, 0), 'capacity': 200},
            ],
            LiveLeadOrderStatus.ONGOING.value: [
                {'day': LiveLeadDeliveryDay.TUESDAY.value, 'start': time_of_day(8, 30), 'end': time_of_day(16, 30), 'capacity': 450},
                {'day': LiveLeadDeliveryDay.THURSDAY.value, 'start': time_of_day(8, 30), 'end': time_of_day(16, 30), 'capacity': 450},
                {'day': LiveLeadDeliveryDay.FRIDAY.value, 'start': time_of_day(10, 0), 'end': time_of_day(14, 0), 'capacity': 200},
            ],
            LiveLeadOrderStatus.COMPLETED.value: [
                {'day': LiveLeadDeliveryDay.MONDAY.value, 'start': time_of_day(7, 0), 'end': time_of_day(11, 0), 'capacity': 120},
                {'day': LiveLeadDeliveryDay.THURSDAY.value, 'start': time_of_day(11, 0), 'end': time_of_day(15, 0), 'capacity': 120},
            ],
            LiveLeadOrderStatus.DISPUTED.value: [
                {'day': LiveLeadDeliveryDay.TUESDAY.value, 'start': time_of_day(9, 0), 'end': time_of_day(13, 0), 'capacity': 220},
                {'day': LiveLeadDeliveryDay.SATURDAY.value, 'start': time_of_day(10, 0), 'end': time_of_day(14, 0), 'capacity': 180},
            ],
        }

        created = 0
        for order in orders:
            configs = status_based_templates.get(order.status) or [
                {'day': LiveLeadDeliveryDay.MONDAY.value, 'start': time_of_day(9, 0), 'end': time_of_day(17, 0), 'capacity': 100},
            ]
            for config in configs:
                schedule = LiveLeadDeliverySchedule(
                    order_id=order.id,
                    day_of_week=config['day'],
                    start_time=config['start'],
                    end_time=config['end'],
                    capacity=config['capacity'],
                )
                db_session.add(schedule)
                created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} live lead delivery schedules into the database")
    finally:
        db_session.close()


def load_live_lead_order_status_history():
    """Backfill lifecycle transitions for seeded live lead orders."""

    db_session = SessionLocal()
    try:
        if db_session.query(LiveLeadOrderStatusHistory).count():
            print('Live lead order status history already exists; skipping history seed')
            return

        orders = {order.order_code: order for order in db_session.query(LiveLeadOrder).all()}
        if not orders:
            print('No live lead orders available; skipping status history seed')
            return

        user_row = db_session.query(User.id).order_by(User.id).first()
        changed_by = user_row[0] if user_row else None

        status_templates = {
            LiveLeadOrderStatus.AWAITING_START_DATE.value: [
                {'status': LiveLeadOrderStatus.AWAITING_START_DATE.value, 'days_after_order': 0, 'remarks': 'Order created'},
                {'status': LiveLeadOrderStatus.API_NOT_CONNECTED.value, 'days_after_order': 2, 'remarks': 'Awaiting API verification'},
            ],
            LiveLeadOrderStatus.ONGOING.value: [
                {'status': LiveLeadOrderStatus.AWAITING_START.value, 'days_after_order': 0, 'remarks': 'Kickoff scheduled'},
                {'status': LiveLeadOrderStatus.ONGOING.value, 'days_after_order': 7, 'remarks': 'Daily delivery established'},
            ],
            LiveLeadOrderStatus.COMPLETED.value: [
                {'status': LiveLeadOrderStatus.AWAITING_START.value, 'days_after_order': 0, 'remarks': 'Pending first delivery'},
                {'status': LiveLeadOrderStatus.ONGOING.value, 'days_after_order': 5, 'remarks': 'Deliveries flowing'},
                {'status': LiveLeadOrderStatus.COMPLETED.value, 'days_after_order': 35, 'remarks': 'Package delivered in full'},
            ],
            LiveLeadOrderStatus.DISPUTED.value: [
                {'status': LiveLeadOrderStatus.ONGOING.value, 'days_after_order': 0, 'remarks': 'Deliveries started'},
                {'status': LiveLeadOrderStatus.DISPUTED.value, 'days_after_order': 12, 'remarks': 'Buyer reported quality issues'},
            ],
        }

        created = 0
        for order in orders.values():
            entries = status_templates.get(order.status)
            if not entries:
                continue

            base_datetime = datetime.combine(order.ordered_on, time_of_day(9, 0)) if order.ordered_on else datetime.utcnow()
            for entry in entries:
                changed_at = base_datetime + timedelta(days=entry.get('days_after_order', 0))
                history = LiveLeadOrderStatusHistory(
                    order_id=order.id,
                    status=entry['status'],
                    changed_at=changed_at,
                    changed_by=changed_by,
                    remarks=entry.get('remarks'),
                )
                db_session.add(history)
                created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} live lead status history rows into the database")
    finally:
        db_session.close()


def load_daily_lead_delivery_logs():
    """Generate mock daily delivery summaries for the seeded live lead orders."""

    db_session = SessionLocal()
    try:
        if db_session.query(DailyLeadDeliveryLog).count():
            print('Daily live lead delivery logs already exist; skipping delivery log seed')
            return

        orders = {order.order_code: order for order in db_session.query(LiveLeadOrder).all()}
        if not orders:
            print('No live lead orders available; skipping delivery log seed')
            return

        log_templates = {
            LiveLeadOrderStatus.AWAITING_START_DATE.value: [],
            LiveLeadOrderStatus.ONGOING.value: [
                {'days_after_start': 1, 'sent': 150, 'success': 140, 'failed': 10, 'status': LiveLeadDeliveryStatus.PARTIAL.value},
                {'days_after_start': 2, 'sent': 180, 'success': 172, 'failed': 8, 'status': LiveLeadDeliveryStatus.COMPLETED.value},
            ],
            LiveLeadOrderStatus.COMPLETED.value: [
                {'days_after_start': 3, 'sent': 200, 'success': 200, 'failed': 0, 'status': LiveLeadDeliveryStatus.COMPLETED.value},
                {'days_after_start': 4, 'sent': 210, 'success': 208, 'failed': 2, 'status': LiveLeadDeliveryStatus.COMPLETED.value},
            ],
            LiveLeadOrderStatus.DISPUTED.value: [
                {'days_after_start': 2, 'sent': 140, 'success': 120, 'failed': 20, 'status': LiveLeadDeliveryStatus.PARTIAL.value},
                {'days_after_start': 3, 'sent': 150, 'success': 110, 'failed': 40, 'status': LiveLeadDeliveryStatus.PARTIAL.value},
            ],
        }

        created = 0
        for order in orders.values():
            entries = log_templates.get(order.status)
            if not entries:
                continue

            base_date = order.start_date or order.ordered_on or datetime.utcnow().date()
            for entry in entries:
                log_date = base_date + timedelta(days=entry.get('days_after_start', 0))
                log_row = DailyLeadDeliveryLog(
                    order_id=order.id,
                    date=log_date,
                    leads_sent=entry['sent'],
                    success_count=entry['success'],
                    failure_count=entry['failed'],
                    delivery_status=entry['status'],
                )
                db_session.add(log_row)
                created += 1

        if created:
            db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {created} daily live lead delivery log rows into the database")
    finally:
        db_session.close()


def load_disputes():
    column_mapping = {
        'Title': 'title',
        'Description': 'description',
        'Dispute Reason': 'dispute_reason',
        'Raised Date': 'raised_date',
        'Resolution Date': 'resolution_date',
        'Status': 'status',
        'Priority': 'priority',
        'Disputed Amount': 'disputed_amount',
        'Refund Amount': 'refund_amount',
        'Compensation Amount': 'compensation_amount',
        'Resolution Notes': 'resolution_notes',
        'Order ID': 'id_order',
        'Product ID': 'id_product',
        'Complainant Company ID': 'id_complainant_company',
        'Respondent Company ID': 'id_respondent_company',
        'Complainant User ID': 'id_complainant_user',
        'Buyer ID': 'id_buyer',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/disputes.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping disputes load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping disputes load")
        return

    db_session = SessionLocal()
    try:
        company_ids = {comp.id for comp in db_session.query(Company).all()}
        user_ids = {user.id for user in db_session.query(User).all()}
        buyer_ids = {buyer.id for buyer in db_session.query(Buyer).all()}
        order_ids = {order.id for order in db_session.query(Order).all()}
        product_ids = {product.id for product in db_session.query(Product).all()}

        required_fields = [
            'title',
            'dispute_reason',
            'raised_date',
            'status',
            'priority',
            'disputed_amount',
            'id_complainant_company',
            'id_respondent_company',
            'id_complainant_user',
        ]

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading disputes", "disputes")

            dispute_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column in ['raised_date', 'resolution_date']:
                        try:
                            parsed_value = pd.to_datetime(value)
                            dispute_data[db_column] = parsed_value
                        except Exception:
                            dispute_data[db_column] = None
                    elif db_column in ['disputed_amount', 'refund_amount', 'compensation_amount']:
                        try:
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            dispute_data[db_column] = float(clean_value)
                        except Exception:
                            dispute_data[db_column] = 0.0 if db_column == 'disputed_amount' else None
                    elif db_column in [
                        'id_order',
                        'id_product',
                        'id_complainant_company',
                        'id_respondent_company',
                        'id_complainant_user',
                        'id_buyer',
                        'id_seller',
                    ]:
                        try:
                            dispute_data[db_column] = int(value)
                        except Exception:
                            dispute_data[db_column] = None
                    else:
                        dispute_data[db_column] = value

            missing_fields = [field for field in required_fields if not dispute_data.get(field)]
            if missing_fields:
                print(
                    "Warning: Missing required fields {} for dispute, skipping".format(
                        ', '.join(missing_fields)
                    )
                )
                continue

            validation_checks = [
                ('id_complainant_company', company_ids, 'Complainant Company', True),
                ('id_respondent_company', company_ids, 'Respondent Company', True),
                ('id_complainant_user', user_ids, 'Complainant User', True),
                ('id_buyer', buyer_ids, 'Buyer', False),
                ('id_order', order_ids, 'Order', False),
                ('id_product', product_ids, 'Product', False),
            ]

            skip_record = False
            for field_name, valid_ids, entity_name, is_required in validation_checks:
                entity_id = dispute_data.get(field_name)

                if entity_id is None:
                    if is_required:
                        print(f"Warning: No {entity_name} ID provided, skipping dispute")
                        skip_record = True
                    continue

                if valid_ids and entity_id not in valid_ids:
                    print(
                        f"Warning: {entity_name} ID {entity_id} not found, skipping dispute"
                    )
                    skip_record = True
                    break

            if skip_record:
                continue

            dispute = Dispute(**dispute_data)
            db_session.add(dispute)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} disputes into the database")
    finally:
        db_session.close()


def load_countries():
    column_mapping = {
        'Name': 'name',
        'Code': 'code',
        'Flag Emoji': 'flag_emoji',
        'Icon ID': 'id_icon',
    }

    csv_path = 'data/csv/countries.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping countries load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping countries load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading countries", "countries")

            country_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    country_data[db_column] = value

            country = Country(**country_data)
            db_session.add(country)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} countries into the database")
    finally:
        db_session.close()


def load_states():
    column_mapping = {
        'Name': 'name',
        'Code': 'code',
        'Country Name': 'country_name',  # We'll resolve this to id_country
    }

    csv_path = 'data/csv/states.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping states load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping states load")
        return

    db_session = SessionLocal()
    try:
        # Get countries for lookup
        countries = {country.name: country.id for country in db_session.query(Country).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading states", "states")

            # Map basic fields
            state_data = {}
            for csv_column, db_column in column_mapping.items():
                if csv_column != 'Country Name':  # Handle country lookup separately
                    value = row.get(csv_column)
                    if pd.notna(value):
                        state_data[db_column] = value

            # Resolve country name to ID
            country_name = row.get('Country Name')
            if pd.notna(country_name) and country_name in countries:
                state_data['id_country'] = countries[country_name]
            else:
                print(f"Warning: Country '{country_name}' not found, skipping state")
                continue

            # Remove the temporary field
            state_data.pop('country_name', None)

            state = State(**state_data)
            db_session.add(state)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} states into the database")
    finally:
        db_session.close()


def load_addresses():
    column_mapping = {
        'Street Address': 'street_address',
        'Address Line 2': 'address_line_2',
        'City': 'city',
        'Postal Code': 'postal_code',
        'Country Name': 'country_name',  # We'll resolve this to id_country
        'State Name': 'state_name',      # We'll resolve this to id_state
    }

    csv_path = 'data/csv/addresses.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping addresses load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping addresses load")
        return

    db_session = SessionLocal()
    try:
        # Get countries and states for lookup
        countries = {country.name: country.id for country in db_session.query(Country).all()}
        states = {state.name: state.id for state in db_session.query(State).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading addresses", "addresses")

            # Map basic fields
            address_data = {}
            for csv_column, db_column in column_mapping.items():
                if csv_column not in ['Country Name', 'State Name']:  # Handle lookups separately
                    value = row.get(csv_column)
                    if pd.notna(value):
                        address_data[db_column] = value

            # Resolve country name to ID
            country_name = row.get('Country Name')
            if pd.notna(country_name) and country_name in countries:
                address_data['id_country'] = countries[country_name]
            else:
                print(f"Warning: Country '{country_name}' not found, skipping address")
                continue

            # Resolve state name to ID (optional)
            state_name = row.get('State Name')
            if pd.notna(state_name) and state_name in states:
                address_data['id_state'] = states[state_name]
            # Note: id_state is nullable, so we don't skip if state is not found

            # Remove the temporary fields
            address_data.pop('country_name', None)
            address_data.pop('state_name', None)

            address = Address(**address_data)
            db_session.add(address)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} addresses into the database")
    finally:
        db_session.close()


def load_companies():
    column_mapping = {
        'Name': 'name',
        'Registration Number': 'registration_number',
        'ICO Number': 'ico_number',
        'ICO Verification Status': 'ico_verification_status',
        'ICO Verified Date': 'ico_verified_date',
        'VAT Number': 'vat_number',
        'VAT Verification Status': 'vat_verification_status',
        'VAT Verified Date': 'vat_verified_date',
        'Status': 'status',
        'Phone': 'phone',
        'GDPR Fines': 'gdpr_fines',
        'Follower Count': 'follower_count',
        'Approval Status': 'approval_status',
        'Signed Up Date': 'signed_up_date',
        'Address ID': 'id_address',  # Direct address ID reference
    }

    csv_path = 'data/csv/companies.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping companies load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping companies load")
        return

    db_session = SessionLocal()
    try:
        # Get addresses for validation
        address_ids = {addr.id for addr in db_session.query(Address).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading companies", "companies")

            company_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column in ['ico_verified_date', 'vat_verified_date', 'signed_up_date']:
                        try:
                            company_data[db_column] = pd.to_datetime(value)
                        except:
                            company_data[db_column] = None
                    # Handle boolean fields
                    elif db_column == 'gdpr_fines':
                        company_data[db_column] = str(value).lower() in ['true', '1', 'yes', 'y']
                    # Handle integer fields
                    elif db_column == 'follower_count':
                        try:
                            company_data[db_column] = int(value)
                        except:
                            company_data[db_column] = 0
                    else:
                        company_data[db_column] = value

            # Validate address ID exists
            address_id = company_data.get('id_address')
            if address_id and address_id not in address_ids:
                print(f"Warning: Address ID {address_id} not found, skipping company")
                continue
            elif not address_id:
                print(f"Warning: No address ID provided, skipping company")
                continue

            company = Company(**company_data)
            db_session.add(company)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} companies into the database")
    finally:
        db_session.close()


def load_company_users():
    column_mapping = {
        'Position': 'position',
        'Is Primary Contact': 'is_primary_contact',
        'Status': 'status',
        'Joined Date': 'joined_date',
        'Company ID': 'id_company',  # Direct company ID reference
        'User ID': 'id_user',        # Direct user ID reference
    }

    csv_path = 'data/csv/company_users.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping company users load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping company users load")
        return

    db_session = SessionLocal()
    try:
        # Get companies and users for validation
        company_ids = {comp.id for comp in db_session.query(Company).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading company users", "company users")

            company_user_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'joined_date':
                        try:
                            company_user_data[db_column] = pd.to_datetime(value)
                        except:
                            company_user_data[db_column] = None
                    # Handle boolean fields
                    elif db_column == 'is_primary_contact':
                        company_user_data[db_column] = str(value).lower() in ['true', '1', 'yes', 'y']
                    else:
                        company_user_data[db_column] = value

            # Validate company ID exists
            company_id = company_user_data.get('id_company')
            if company_id and company_id not in company_ids:
                print(f"Warning: Company ID {company_id} not found, skipping company user")
                continue
            elif not company_id:
                print(f"Warning: No company ID provided, skipping company user")
                continue

            # Validate user ID exists
            user_id = company_user_data.get('id_user')
            if user_id and user_id not in user_ids:
                print(f"Warning: User ID {user_id} not found, skipping company user")
                continue
            elif not user_id:
                print(f"Warning: No user ID provided, skipping company user")
                continue

            company_user = CompanyUser(**company_user_data)
            db_session.add(company_user)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} company users into the database")
    finally:
        db_session.close()


def load_buyers():
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'User Status': 'user_status',
        'Company ID': 'id_company',
        'Status': 'status',
        'Total Purchases': 'total_purchases',
        'Total Disputes': 'total_disputes',
        'First Purchase Date': 'first_purchase_date',
        'Last Purchase Date': 'last_purchase_date',
        'Notes': 'notes',
    }

    csv_path = 'data/csv/buyers.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyers load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyers load")
        return

    db_session = SessionLocal()
    try:
        company_ids = {company.id for company in db_session.query(Company).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyers", "buyers")

            buyer_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column == 'id_company':
                        try:
                            buyer_data[db_column] = int(value)
                        except Exception:
                            buyer_data[db_column] = None
                    elif db_column in ['total_purchases', 'total_disputes']:
                        try:
                            buyer_data[db_column] = int(value)
                        except Exception:
                            buyer_data[db_column] = 0
                    elif db_column in ['first_purchase_date', 'last_purchase_date']:
                        try:
                            buyer_data[db_column] = pd.to_datetime(value)
                        except Exception:
                            buyer_data[db_column] = None
                    else:
                        buyer_data[db_column] = str(value).strip()

            company_id = buyer_data.get('id_company')
            name = buyer_data.get('name')
            email = buyer_data.get('email')

            if not name:
                print("Warning: No name provided, skipping buyer")
                continue
            if not email:
                print("Warning: No email provided, skipping buyer")
                continue
            if not company_id:
                print("Warning: No Company ID provided, skipping buyer")
                continue
            if company_id not in company_ids:
                print(f"Warning: Company ID {company_id} not found, skipping buyer")
                continue

            buyer = Buyer(**buyer_data)
            db_session.add(buyer)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyers into the database")
    finally:
        db_session.close()




def load_sellers():
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Position': 'position',
        'User Status': 'user_status',
        'Seller Status': 'seller_status',
        'Company ID': 'id_company',
        'Total Listings': 'total_listings',
        'Total Sales': 'total_sales',
        'Rating': 'rating',
    }

    csv_path = 'data/csv/sellers.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping sellers load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping sellers load")
        return

    db_session = SessionLocal()
    try:
        company_ids = {company.id for company in db_session.query(Company).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading sellers", "sellers")

            seller_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column == 'id_company':
                        try:
                            seller_data[db_column] = int(value)
                        except Exception:
                            seller_data[db_column] = None
                    elif db_column in ['total_listings', 'total_sales']:
                        try:
                            seller_data[db_column] = int(value)
                        except Exception:
                            seller_data[db_column] = 0
                    elif db_column == 'rating':
                        try:
                            seller_data[db_column] = float(value)
                        except Exception:
                            seller_data[db_column] = None
                    else:
                        seller_data[db_column] = str(value).strip()

            company_id = seller_data.get('id_company')
            name = seller_data.get('name')
            email = seller_data.get('email')

            if not name:
                print("Warning: No name provided, skipping seller")
                continue
            if not email:
                print("Warning: No email provided, skipping seller")
                continue
            if not company_id:
                print("Warning: No Company ID provided, skipping seller")
                continue
            if company_id not in company_ids:
                print(f"Warning: Company ID {company_id} not found, skipping seller")
                continue

            seller = Seller(**seller_data)
            db_session.add(seller)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} sellers into the database")
    finally:
        db_session.close()




def load_dd_users():
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Role': 'role',
        'Invited By': 'invited_by',
        'Total Checks': 'total_checks',
        'Amount Spend': 'amount_spend',
        'Status': 'status',
        'Total Verifications': 'total_verifications',
        'Total DD Verify': 'total_dd_verify',
        'Total KYC Verify': 'total_kyc_verify',
        'Verified Leads': 'verified_leads',
        'Non-Compliant Leads': 'non_compliant_leads',
        'Rejected Leads': 'rejected_leads',
        'Credits Remaining': 'credits_remaining',
        'Last KYC Verify': 'last_kyc_verify',
        'Lead Source Details': 'lead_source_details',
        'Top Lead Sources': 'top_lead_sources',
        'Most Checked Source': 'most_checked_source',
        'Lowest Performing Score': 'lowest_performing_score',
    }

    csv_path = 'data/csv/dd_users.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping dd users load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping dd users load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading DD users", "dd users")

            dd_user_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.isna(value):
                    continue

                if db_column in [
                    'total_checks',
                    'total_verifications',
                    'total_dd_verify',
                    'total_kyc_verify',
                    'verified_leads',
                    'non_compliant_leads',
                    'rejected_leads',
                ]:
                    try:
                        dd_user_data[db_column] = int(value)
                    except Exception:
                        dd_user_data[db_column] = 0
                elif db_column in ['amount_spend', 'credits_remaining', 'lowest_performing_score']:
                    try:
                        dd_user_data[db_column] = float(value)
                    except Exception:
                        dd_user_data[db_column] = 0.0
                elif db_column == 'last_kyc_verify':
                    try:
                        dd_user_data[db_column] = pd.to_datetime(value)
                    except Exception:
                        dd_user_data[db_column] = None
                elif db_column in ['lead_source_details', 'top_lead_sources'] and isinstance(value, str):
                    try:
                        dd_user_data[db_column] = json.loads(value)
                    except json.JSONDecodeError:
                        dd_user_data[db_column] = None
                else:
                    dd_user_data[db_column] = value

            dd_user = DDUser(**dd_user_data)
            db_session.add(dd_user)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} DD users into the database")
    finally:
        db_session.close()
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Position': 'position',
        'User Status': 'user_status',
        'Seller Status': 'seller_status',
        'Company ID': 'id_company',
        'Total Listings': 'total_listings',
        'Total Sales': 'total_sales',
        'Rating': 'rating',
    }

    csv_path = 'data/csv/sellers.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping sellers load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping sellers load")
        return

    db_session = SessionLocal()
    try:
        company_ids = {company.id for company in db_session.query(Company).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading sellers", "sellers")

            seller_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column == 'id_company':
                        try:
                            seller_data[db_column] = int(value)
                        except Exception:
                            seller_data[db_column] = None
                    elif db_column in ['total_listings', 'total_sales']:
                        try:
                            seller_data[db_column] = int(value)
                        except Exception:
                            seller_data[db_column] = 0
                    elif db_column == 'rating':
                        try:
                            seller_data[db_column] = float(value)
                        except Exception:
                            seller_data[db_column] = None
                    else:
                        seller_data[db_column] = str(value).strip()

            company_id = seller_data.get('id_company')
            name = seller_data.get('name')
            email = seller_data.get('email')

            if not name:
                print("Warning: No name provided, skipping seller")
                continue
            if not email:
                print("Warning: No email provided, skipping seller")
                continue
            if not company_id:
                print("Warning: No Company ID provided, skipping seller")
                continue
            if company_id not in company_ids:
                print(f"Warning: Company ID {company_id} not found, skipping seller")
                continue

            seller = Seller(**seller_data)
            db_session.add(seller)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} sellers into the database")
    finally:
        db_session.close()


def load_products():
    column_mapping = {
        'Name': 'name',
        'Description': 'description',
        'Product Type': 'product_type',
        'Price': 'price',
        'Pricing Tiers': 'pricing_tiers',
        'Daily Quantity': 'daily_quantity',
        'Minimum Quantity': 'minimum_quantity',
        'Available Leads Next 7 Days': 'available_leads_next_7_days',
        'Lead Availability Schedule': 'lead_availability_schedule',
        'Total Records': 'total_records',
        'Available Records': 'available_records',
        'Contact Methods': 'contact_methods',
        'Replacement Policy': 'replacement_policy',
        'Data Source Name': 'data_source_name',
        'Listing Period Months': 'listing_period_months',
        'License Period Months': 'license_period_months',
        'Usage Limit Type': 'usage_limit_type',
        'Data Type': 'data_type',
        'Sale Type': 'sale_type',
        'Geographic Coverage': 'geographic_coverage',
        'Restricted Use': 'restricted_use',
        'Source URL': 'source_url',
        'Uploaded Date': 'uploaded_date',
        'TPS Check Status': 'tps_check_status',
        'MPS Check Status': 'mps_check_status',
        'HLR Check Status': 'hlr_check_status',
        'LLV Check Status': 'llv_check_status',
        'Geo Validation Status': 'geo_validation_status',
        'Suppression Check Status': 'suppression_check_status',
        'GDPR Consent Status': 'gdpr_consent_status',
        'View Count': 'view_count',
        'Favorite Count': 'favorite_count',
        'Rating Average': 'rating_average',
        'Status': 'status',
        'Company ID': 'id_company',
        'Category ID': 'id_category',
        'Sub Category ID': 'id_sub_category',
        'Selection ID': 'id_selection',
        'Created By User ID': 'id_created_by_user',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/products.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping products load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping products load")
        return

    db_session = SessionLocal()
    try:
        company_ids = {comp.id for comp in db_session.query(Company).all()}
        category_ids = {cat.id for cat in db_session.query(Category).all()}
        sub_category_ids = {sub.id for sub in db_session.query(SubCategory).all()}
        selection_ids = {sel.id for sel in db_session.query(Selection).all()}
        user_ids = {user.id for user in db_session.query(User).all()}
        seller_ids = {seller.id for seller in db_session.query(Seller).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading products", "products")

            product_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    if db_column in ['price', 'rating_average']:
                        try:
                            product_data[db_column] = float(value)
                        except Exception:
                            product_data[db_column] = None
                    elif db_column in [
                        'daily_quantity',
                        'minimum_quantity',
                        'available_leads_next_7_days',
                        'total_records',
                        'available_records',
                        'listing_period_months',
                        'license_period_months',
                        'view_count',
                        'favorite_count',
                        'id_company',
                        'id_category',
                        'id_sub_category',
                        'id_selection',
                        'id_created_by_user',
                        'id_seller',
                    ]:
                        try:
                            product_data[db_column] = int(value)
                        except Exception:
                            product_data[db_column] = None
                    elif db_column == 'uploaded_date':
                        try:
                            product_data[db_column] = pd.to_datetime(value)
                        except Exception:
                            product_data[db_column] = None
                    elif db_column in ['pricing_tiers', 'lead_availability_schedule']:
                        if isinstance(value, str):
                            try:
                                product_data[db_column] = json.loads(value)
                            except json.JSONDecodeError:
                                product_data[db_column] = None
                        else:
                            product_data[db_column] = value
                    else:
                        product_data[db_column] = value

            validation_checks = [
                ('id_company', company_ids, 'Company', True),
                ('id_category', category_ids, 'Category', True),
                ('id_sub_category', sub_category_ids, 'Sub Category', True),
                ('id_selection', selection_ids, 'Selection', True),
                ('id_created_by_user', user_ids, 'Created By User', True),
                ('id_seller', seller_ids, 'Seller', False),
            ]

            skip_record = False
            for field_name, valid_ids, entity_name, is_required in validation_checks:
                entity_id = product_data.get(field_name)
                if entity_id is None:
                    if is_required:
                        print(f"Warning: No {entity_name} ID provided, skipping product")
                        skip_record = True
                        break
                    continue
                if valid_ids and entity_id not in valid_ids:
                    print(f"Warning: {entity_name} ID {entity_id} not found, skipping product")
                    skip_record = True
                    break

            if skip_record:
                continue

            product = Product(**product_data)
            db_session.add(product)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} products into the database")
    finally:
        db_session.close()



def load_templates():
    column_mapping = {
        'Name': 'name',
        'Description': 'description',
        'Channel': 'channel',
        'Status': 'status',
        'Subject': 'subject',
        'Body': 'body',
        'Has Attachment': 'has_attachment',
        'Agent Active': 'agent_active',
        'Client View': 'client_view',
        'Template Type': 'template_type',
        'Character Count': 'character_count',
        'Agent Send': 'agent_send',
        'Marketing': 'marketing',
        'Version': 'version',
        'Last Published At': 'last_published_at',
        'Created By User ID': 'id_created_by_user',
    }

    csv_path = 'data/csv/templates.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping templates load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping templates load")
        return

    df = df.reset_index(drop=True)

    db_session = SessionLocal()
    try:
        user_ids = {user.id for user in db_session.query(User).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading templates", "templates")

            template_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.isna(value):
                    continue

                if db_column in ['has_attachment', 'agent_active', 'client_view', 'agent_send', 'marketing']:
                    template_data[db_column] = str(value).strip().lower() in ['true', '1', 'yes']
                elif db_column in ['character_count', 'version', 'id_created_by_user']:
                    try:
                        template_data[db_column] = int(value)
                    except Exception:
                        template_data[db_column] = None
                elif db_column == 'last_published_at':
                    try:
                        template_data[db_column] = pd.to_datetime(value)
                    except Exception:
                        template_data[db_column] = None
                else:
                    template_data[db_column] = value

            created_by = template_data.get('id_created_by_user')
            if not created_by or created_by not in user_ids:
                print('Warning: Invalid created by user ID, skipping template')
                continue

            template = Template(**template_data)
            db_session.add(template)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} templates into the database")
    finally:
        db_session.close()


def load_offensive_words():
    column_mapping = {
        'Word': 'word',
        'Severity': 'severity',
        'Active': 'is_active',
        'Added Date': 'added_date',
        'Usage Count': 'usage_count',
        'Description': 'description',
        'Created By User ID': 'id_created_by_user',
    }

    csv_path = 'data/csv/offensive_words.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping offensive words load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping offensive words load")
        return

    df = df.reset_index(drop=True)

    valid_severities = {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'}

    db_session = SessionLocal()
    try:
        user_ids = {user.id for user in db_session.query(User).all()}

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading offensive words", "offensive words")

            offensive_word_data = {}
            skip_record = False

            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.isna(value):
                    continue

                if db_column == 'severity':
                    normalized_value = str(value).strip().upper()
                    if normalized_value not in valid_severities:
                        print(f"Warning: Invalid severity '{value}', skipping offensive word")
                        skip_record = True
                        break
                    offensive_word_data[db_column] = normalized_value
                elif db_column == 'is_active':
                    offensive_word_data[db_column] = str(value).strip().lower() in ['true', '1', 'yes']
                elif db_column in ['usage_count', 'id_created_by_user']:
                    try:
                        offensive_word_data[db_column] = int(value)
                    except Exception:
                        offensive_word_data[db_column] = None
                elif db_column == 'added_date':
                    try:
                        offensive_word_data[db_column] = pd.to_datetime(value)
                    except Exception:
                        offensive_word_data[db_column] = None
                else:
                    offensive_word_data[db_column] = str(value).strip()

            if skip_record:
                continue

            user_id = offensive_word_data.get('id_created_by_user')
            if user_id is None or user_id not in user_ids:
                print(f"Warning: User ID {user_id} not found, skipping offensive word")
                continue

            offensive_word = OffensiveWord(**offensive_word_data)
            db_session.add(offensive_word)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} offensive words into the database")
    finally:
        db_session.close()


def load_reviews():
    column_mapping = {
        'Title': 'title',
        'Review Text': 'review_text',
        'Review Date': 'review_date',
        'Recommended': 'is_recommended',
        'Accuracy Rating': 'accuracy_rating',
        'Receptivity Rating': 'receptivity_rating',
        'Contact Rate Rating': 'contact_rate_rating',
        'Overall Rating': 'overall_rating',
        'Reported Count': 'reported_count',
        'Is Flagged': 'is_flagged',
        'Contains Offensive Words': 'contains_offensive_words',
        'Moderation Notes': 'moderation_notes',
        'Status': 'status',
        'Product ID': 'id_product',
        'Reviewer User ID': 'id_reviewer_user',
        'Reviewer Company ID': 'id_reviewer_company',
        'Order ID': 'id_order',
    }

    csv_path = 'data/csv/reviews.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping reviews load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping reviews load")
        return

    db_session = SessionLocal()
    try:
        product_ids = {product.id for product in db_session.query(Product).all()}
        user_ids = {user.id for user in db_session.query(User).all()}
        company_ids = {company.id for company in db_session.query(Company).all()}
        order_ids = {order.id for order in db_session.query(Order).all()}

        required_fields = [
            'review_text',
            'review_date',
            'is_recommended',
            'overall_rating',
            'id_product',
            'id_reviewer_user',
            'id_reviewer_company',
        ]

        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading reviews", "reviews")

            review_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.isna(value):
                    continue

                if db_column == 'review_date':
                    try:
                        review_data[db_column] = pd.to_datetime(value)
                    except Exception:
                        review_data[db_column] = None
                elif db_column in ['accuracy_rating', 'receptivity_rating', 'contact_rate_rating', 'overall_rating']:
                    try:
                        review_data[db_column] = float(value)
                    except Exception:
                        review_data[db_column] = None
                elif db_column == 'reported_count':
                    try:
                        review_data[db_column] = int(value)
                    except Exception:
                        review_data[db_column] = 0
                elif db_column in ['is_recommended', 'is_flagged', 'contains_offensive_words']:
                    review_data[db_column] = str(value).strip().lower() in ['true', '1', 'yes', 'y']
                elif db_column in ['id_product', 'id_reviewer_user', 'id_reviewer_company', 'id_order']:
                    try:
                        review_data[db_column] = int(value)
                    except Exception:
                        review_data[db_column] = None
                else:
                    review_data[db_column] = value

            missing_fields = []
            for field in required_fields:
                if field not in review_data or review_data[field] is None:
                    missing_fields.append(field)
                elif isinstance(review_data[field], str) and not review_data[field].strip():
                    missing_fields.append(field)

            if missing_fields:
                print(
                    "Warning: Missing required fields {} for review, skipping".format(
                        ', '.join(sorted(set(missing_fields)))
                    )
                )
                continue

            if review_data.get('reported_count') is None:
                review_data['reported_count'] = 0

            validation_checks = [
                ('id_product', product_ids, 'Product', True),
                ('id_reviewer_user', user_ids, 'Reviewer User', True),
                ('id_reviewer_company', company_ids, 'Reviewer Company', True),
                ('id_order', order_ids, 'Order', False),
            ]

            skip_record = False
            for field_name, valid_ids, entity_name, is_required in validation_checks:
                entity_id = review_data.get(field_name)

                if entity_id is None:
                    if is_required:
                        print(f"Warning: No {entity_name} ID provided, skipping review")
                        skip_record = True
                    continue

                if valid_ids and entity_id not in valid_ids:
                    print(f"Warning: {entity_name} ID {entity_id} not found, skipping review")
                    skip_record = True
                    break

            if skip_record:
                continue

            review = Review(**review_data)
            db_session.add(review)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} reviews into the database")
    finally:
        db_session.close()


def load_buyer_reports():
    column_mapping = {
        'ID Buyer': 'id_buyer',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Leads Orders': 'leads_orders',
        'Product Orders': 'product_orders',
        'Total Spent': 'total_spent',
        'Status': 'status',
    }

    csv_path = 'data/csv/buyer_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyer reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyer reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyer reports", "reports")

            buyer_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'signed_up_date':
                        try:
                            buyer_report_data[db_column] = pd.to_datetime(value)
                        except:
                            buyer_report_data[db_column] = None
                    # Handle numeric fields
                    elif db_column in ['leads_orders', 'product_orders']:
                        try:
                            buyer_report_data[db_column] = int(value)
                        except:
                            buyer_report_data[db_column] = 0
                    elif db_column == 'total_spent':
                        try:
                            buyer_report_data[db_column] = float(value)
                        except:
                            buyer_report_data[db_column] = 0.00
                    else:
                        buyer_report_data[db_column] = value

            buyer_report = BuyerReport(**buyer_report_data)
            db_session.add(buyer_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyer reports into the database")
    finally:
        db_session.close()


def load_buyer_dispute_reports():
    column_mapping = {
        'ID Buyer': 'id_buyer',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Leads Orders': 'leads_orders',
        'Product Orders': 'product_orders',
        'Disputes': 'disputes',
        'Status': 'status',
    }

    csv_path = 'data/csv/buyer_dispute_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyer dispute reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyer dispute reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyer dispute reports", "reports")

            buyer_dispute_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'signed_up_date':
                        try:
                            buyer_dispute_report_data[db_column] = pd.to_datetime(value)
                        except:
                            buyer_dispute_report_data[db_column] = None
                    # Handle numeric fields
                    elif db_column in ['leads_orders', 'product_orders', 'disputes']:
                        try:
                            buyer_dispute_report_data[db_column] = int(value)
                        except:
                            buyer_dispute_report_data[db_column] = 0
                    else:
                        buyer_dispute_report_data[db_column] = value

            buyer_dispute_report = BuyerDisputeReport(**buyer_dispute_report_data)
            db_session.add(buyer_dispute_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyer dispute reports into the database")
    finally:
        db_session.close()


def load_buyer_purchase_activity_reports():
    column_mapping = {
        'ID Buyer': 'id_buyer',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Last 7 Days': 'last_7_days',
        'Last 30 Days': 'last_30_days',
        'Total YTD': 'total_ytd',
        'Status': 'status',
    }

    csv_path = 'data/csv/buyer_purchase_activity_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyer purchase activity reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyer purchase activity reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyer purchase activity reports", "reports")

            buyer_purchase_activity_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'signed_up_date':
                        try:
                            buyer_purchase_activity_report_data[db_column] = pd.to_datetime(value)
                        except:
                            buyer_purchase_activity_report_data[db_column] = None
                    # Handle currency fields
                    elif db_column in ['last_7_days', 'last_30_days', 'total_ytd']:
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            buyer_purchase_activity_report_data[db_column] = float(clean_value)
                        except:
                            buyer_purchase_activity_report_data[db_column] = 0.00
                    else:
                        buyer_purchase_activity_report_data[db_column] = value

            buyer_purchase_activity_report = BuyerPurchaseActivityReport(**buyer_purchase_activity_report_data)
            db_session.add(buyer_purchase_activity_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyer purchase activity reports into the database")
    finally:
        db_session.close()


def load_buyer_review_activity_reports():
    column_mapping = {
        'ID Buyer': 'id_buyer',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Reviews Left': 'reviews_left',
        'Avg Rating Given': 'avg_rating_given',
        'Negative Reviews': 'negative_reviews',
        'Last Review Date': 'last_review_date',
        'Status': 'status',
    }

    csv_path = 'data/csv/buyer_review_activity_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyer review activity reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyer review activity reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyer review activity reports", "reports")

            buyer_review_activity_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            buyer_review_activity_report_data[db_column] = pd.to_datetime(value)
                        except:
                            buyer_review_activity_report_data[db_column] = None
                    # Handle date fields
                    elif db_column == 'last_review_date':
                        try:
                            buyer_review_activity_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            buyer_review_activity_report_data[db_column] = None
                    # Handle integer fields
                    elif db_column in ['reviews_left', 'negative_reviews']:
                        try:
                            buyer_review_activity_report_data[db_column] = int(value)
                        except:
                            buyer_review_activity_report_data[db_column] = 0
                    # Handle rating field
                    elif db_column == 'avg_rating_given':
                        try:
                            buyer_review_activity_report_data[db_column] = float(value)
                        except:
                            buyer_review_activity_report_data[db_column] = 0.0
                    else:
                        buyer_review_activity_report_data[db_column] = value

            buyer_review_activity_report = BuyerReviewActivityReport(**buyer_review_activity_report_data)
            db_session.add(buyer_review_activity_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyer review activity reports into the database")
    finally:
        db_session.close()


def load_buyer_purchase_breakdown_reports():
    column_mapping = {
        'ID Buyer': 'id_buyer',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Solar Leads': 'solar_leads',
        'Finance Leads': 'finance_leads',
        'Home Improvement': 'home_improvement',
        'Others': 'others',
        'Status': 'status',
    }

    csv_path = 'data/csv/buyer_purchase_breakdown_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping buyer purchase breakdown reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping buyer purchase breakdown reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading buyer purchase breakdown reports", "reports")

            buyer_purchase_breakdown_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            buyer_purchase_breakdown_report_data[db_column] = pd.to_datetime(value)
                        except:
                            buyer_purchase_breakdown_report_data[db_column] = None
                    # Handle integer count fields
                    elif db_column in ['solar_leads', 'finance_leads', 'home_improvement', 'others']:
                        try:
                            buyer_purchase_breakdown_report_data[db_column] = int(value)
                        except:
                            buyer_purchase_breakdown_report_data[db_column] = 0
                    else:
                        buyer_purchase_breakdown_report_data[db_column] = value

            buyer_purchase_breakdown_report = BuyerPurchaseBreakdownReport(**buyer_purchase_breakdown_report_data)
            db_session.add(buyer_purchase_breakdown_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} buyer purchase breakdown reports into the database")
    finally:
        db_session.close()


def load_seller_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Total Listing': 'total_listing',
        'Total Orders': 'total_orders',
        'Leads Sold': 'leads_sold',
        'Delivery Rate': 'delivery_rate',
        'Dispute Rate': 'dispute_rate',
        'Avg CPL': 'avg_cpl',
        'Total Sales': 'total_sales',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller reports", "reports")

            seller_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            seller_report_data[db_column] = pd.to_datetime(value)
                        except:
                            seller_report_data[db_column] = None
                    # Handle integer fields
                    elif db_column in ['total_listing', 'total_orders', 'leads_sold']:
                        try:
                            seller_report_data[db_column] = int(value)
                        except:
                            seller_report_data[db_column] = 0
                    # Handle percentage fields
                    elif db_column in ['delivery_rate', 'dispute_rate']:
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            seller_report_data[db_column] = float(clean_value)
                        except:
                            seller_report_data[db_column] = 0.00
                    # Handle currency fields
                    elif db_column in ['avg_cpl', 'total_sales']:
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            seller_report_data[db_column] = float(clean_value)
                        except:
                            seller_report_data[db_column] = 0.00
                    else:
                        seller_report_data[db_column] = value

            seller_report = SellerReport(**seller_report_data)
            db_session.add(seller_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller reports into the database")
    finally:
        db_session.close()


def load_seller_rating_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Total Listing': 'total_listing',
        'Total Orders': 'total_orders',
        'Review Count': 'review_count',
        'Avg Rating': 'avg_rating',
        'Last Reviewed Product': 'last_reviewed_product',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_rating_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller rating reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller rating reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller rating reports", "reports")

            seller_rating_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            seller_rating_report_data[db_column] = pd.to_datetime(value)
                        except:
                            seller_rating_report_data[db_column] = None
                    # Handle integer fields
                    elif db_column in ['total_listing', 'total_orders', 'review_count']:
                        try:
                            seller_rating_report_data[db_column] = int(value)
                        except:
                            seller_rating_report_data[db_column] = 0
                    # Handle rating field
                    elif db_column == 'avg_rating':
                        try:
                            seller_rating_report_data[db_column] = float(value)
                        except:
                            seller_rating_report_data[db_column] = 0.0
                    else:
                        seller_rating_report_data[db_column] = value

            seller_rating_report = SellerRatingReport(**seller_rating_report_data)
            db_session.add(seller_rating_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller rating reports into the database")
    finally:
        db_session.close()


def load_seller_dispute_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Total Listing': 'total_listing',
        'Total Orders': 'total_orders',
        'Delivery Rate': 'delivery_rate',
        'Dispute Received': 'dispute_received',
        'Dispute Rate': 'dispute_rate',
        'Resolved Percentage': 'resolved_percentage',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_dispute_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller dispute reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller dispute reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller dispute reports", "reports")

            seller_dispute_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            seller_dispute_report_data[db_column] = pd.to_datetime(value)
                        except:
                            seller_dispute_report_data[db_column] = None
                    # Handle integer fields
                    elif db_column in ['total_listing', 'total_orders', 'dispute_received']:
                        try:
                            seller_dispute_report_data[db_column] = int(value)
                        except:
                            seller_dispute_report_data[db_column] = 0
                    # Handle percentage fields
                    elif db_column in ['delivery_rate', 'dispute_rate', 'resolved_percentage']:
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            seller_dispute_report_data[db_column] = float(clean_value)
                        except:
                            seller_dispute_report_data[db_column] = 0.00
                    else:
                        seller_dispute_report_data[db_column] = value

            seller_dispute_report = SellerDisputeReport(**seller_dispute_report_data)
            db_session.add(seller_dispute_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller dispute reports into the database")
    finally:
        db_session.close()


def load_seller_dispute_breakdown_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Dispute Received': 'dispute_received',
        'Bad Contact': 'bad_contact',
        'Invalid Data': 'invalid_data',
        'Criteria Mismatch': 'criteria_mismatch',
        'Others': 'others',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_dispute_breakdown_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller dispute breakdown reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller dispute breakdown reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller dispute breakdown reports", "reports")

            seller_dispute_breakdown_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column == 'signed_up_date':
                        try:
                            seller_dispute_breakdown_report_data[db_column] = pd.to_datetime(value)
                        except:
                            seller_dispute_breakdown_report_data[db_column] = None
                    # Handle integer count fields
                    elif db_column in ['dispute_received', 'bad_contact', 'invalid_data', 'criteria_mismatch', 'others']:
                        try:
                            seller_dispute_breakdown_report_data[db_column] = int(value)
                        except:
                            seller_dispute_breakdown_report_data[db_column] = 0
                    else:
                        seller_dispute_breakdown_report_data[db_column] = value

            seller_dispute_breakdown_report = SellerDisputeBreakdownReport(**seller_dispute_breakdown_report_data)
            db_session.add(seller_dispute_breakdown_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller dispute breakdown reports into the database")
    finally:
        db_session.close()


def load_seller_listing_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Signed Up Date': 'signed_up_date',
        'Total Listing': 'total_listing',
        'Live Leads': 'live_leads',
        'Dataset': 'dataset',
        'Delivery Rate': 'delivery_rate',
        'Cap Hit Rate': 'cap_hit_rate',
        'Last Uploaded On': 'last_uploaded_on',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_listing_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller listing reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller listing reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller listing reports", "reports")

            seller_listing_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle datetime fields
                    if db_column in ['signed_up_date', 'last_uploaded_on']:
                        try:
                            seller_listing_report_data[db_column] = pd.to_datetime(value)
                        except:
                            seller_listing_report_data[db_column] = None
                    # Handle integer count fields
                    elif db_column in ['total_listing', 'live_leads', 'dataset']:
                        try:
                            seller_listing_report_data[db_column] = int(value)
                        except:
                            seller_listing_report_data[db_column] = 0
                    # Handle percentage fields
                    elif db_column in ['delivery_rate', 'cap_hit_rate']:
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            seller_listing_report_data[db_column] = float(clean_value)
                        except:
                            seller_listing_report_data[db_column] = 0.00
                    else:
                        seller_listing_report_data[db_column] = value

            seller_listing_report = SellerListingReport(**seller_listing_report_data)
            db_session.add(seller_listing_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller listing reports into the database")
    finally:
        db_session.close()


def load_seller_product_performance_reports():
    column_mapping = {
        'ID Seller': 'id_seller',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Product Listing': 'product_listing',
        'Type': 'listing_type',
        'Leads Sold': 'leads_sold',
        'Dispute Rate': 'dispute_rate',
        'Cap Hit Rate': 'cap_hit_rate',
        'Refund Rate': 'refund_rate',
        'Avg Rating': 'avg_rating',
        'Status': 'status',
    }

    csv_path = 'data/csv/seller_product_performance_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping seller product performance reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping seller product performance reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading seller product performance reports", "reports")

            seller_product_performance_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle integer count fields
                    if db_column == 'leads_sold':
                        try:
                            seller_product_performance_report_data[db_column] = int(value)
                        except:
                            seller_product_performance_report_data[db_column] = 0
                    # Handle percentage fields
                    elif db_column in ['dispute_rate', 'cap_hit_rate', 'refund_rate']:
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            seller_product_performance_report_data[db_column] = float(clean_value)
                        except:
                            seller_product_performance_report_data[db_column] = 0.00
                    # Handle rating field
                    elif db_column == 'avg_rating':
                        try:
                            seller_product_performance_report_data[db_column] = float(value)
                        except:
                            seller_product_performance_report_data[db_column] = 0.0
                    else:
                        seller_product_performance_report_data[db_column] = value

            seller_product_performance_report = SellerProductPerformanceReport(**seller_product_performance_report_data)
            db_session.add(seller_product_performance_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} seller product performance reports into the database")
    finally:
        db_session.close()


def load_top_credits_usage_reports():
    column_mapping = {
        'ID User': 'id_user',
        'User Name': 'user_name',
        'User Email': 'user_email',
        'Credit Used': 'credit_used',
        'Credit Purchased': 'credit_purchased',
        'Remaining Credits': 'remaining_credits',
        'Spent On Credits': 'spent_on_credits',
        'Last Top Up': 'last_top_up',
        'Status': 'status',
    }

    csv_path = 'data/csv/top_credits_usage_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping top credits usage reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping top credits usage reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading top credits usage reports", "reports")

            top_credits_usage_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date fields
                    if db_column == 'last_top_up':
                        try:
                            top_credits_usage_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            top_credits_usage_report_data[db_column] = None
                    # Handle integer credit fields
                    elif db_column in ['credit_used', 'credit_purchased', 'remaining_credits']:
                        try:
                            top_credits_usage_report_data[db_column] = int(value)
                        except:
                            top_credits_usage_report_data[db_column] = 0
                    # Handle currency field
                    elif db_column == 'spent_on_credits':
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            top_credits_usage_report_data[db_column] = float(clean_value)
                        except:
                            top_credits_usage_report_data[db_column] = 0.00
                    else:
                        top_credits_usage_report_data[db_column] = value

            top_credits_usage_report = TopCreditsUsageReport(**top_credits_usage_report_data)
            db_session.add(top_credits_usage_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} top credits usage reports into the database")
    finally:
        db_session.close()


def load_check_type_reports():
    column_mapping = {
        'Check Type': 'check_type',
        'Total Checks': 'total_checks',
        'Successful Checks': 'successful_checks',
        'Failed Checks': 'failed_checks',
        'Success Rate(%)': 'success_rate',
        'Most Common Error': 'most_common_error',
        'Status': 'status',
    }

    csv_path = 'data/csv/check_type_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping check type reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping check type reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading check type reports", "reports")

            check_type_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle integer fields
                    if db_column in ['total_checks', 'successful_checks', 'failed_checks']:
                        try:
                            check_type_report_data[db_column] = int(value)
                        except:
                            check_type_report_data[db_column] = 0
                    # Handle percentage field
                    elif db_column == 'success_rate':
                        try:
                            # Remove percentage symbol if present
                            clean_value = str(value).replace('%', '').strip()
                            check_type_report_data[db_column] = float(clean_value)
                        except:
                            check_type_report_data[db_column] = 0.00
                    else:
                        check_type_report_data[db_column] = value

            check_type_report = CheckTypeReport(**check_type_report_data)
            db_session.add(check_type_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} check type reports into the database")
    finally:
        db_session.close()


def load_revenue_trend_reports():
    column_mapping = {
        'Date': 'date',
        'Revenue': 'revenue',
        'Seller ID': 'id_seller',
    }

    csv_path = 'data/csv/revenue_trend_reports.csv'
    if not os.path.exists(csv_path):
        print(f"Info: {csv_path} not found, skipping revenue trend reports load")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print(f"Warning: Failed to read {csv_path}, skipping revenue trend reports load")
        return

    db_session = SessionLocal()
    try:
        for index, row in df.iterrows():
            ProgressDisplay.show_progress(index + 1, len(df), "Loading revenue trend reports", "reports")

            revenue_trend_report_data = {}
            for csv_column, db_column in column_mapping.items():
                value = row.get(csv_column)
                if pd.notna(value):
                    # Handle date field
                    if db_column == 'date':
                        try:
                            revenue_trend_report_data[db_column] = pd.to_datetime(value).date()
                        except:
                            revenue_trend_report_data[db_column] = None
                    # Handle revenue amount
                    elif db_column == 'revenue':
                        try:
                            # Remove currency symbols and commas if present
                            clean_value = str(value).replace('£', '').replace(',', '').strip()
                            revenue_trend_report_data[db_column] = float(clean_value)
                        except:
                            revenue_trend_report_data[db_column] = 0.00
                    # Handle seller ID (nullable)
                    elif db_column == 'id_seller':
                        try:
                            revenue_trend_report_data[db_column] = int(value) if value else None
                        except:
                            revenue_trend_report_data[db_column] = None
                    else:
                        revenue_trend_report_data[db_column] = value

            revenue_trend_report = RevenueTrendReport(**revenue_trend_report_data)
            db_session.add(revenue_trend_report)

        db_session.commit()
        ProgressDisplay.finalize_line(f"Loaded {len(df)} revenue trend reports into the database")
    finally:
        db_session.close()

def run_rebuild(export_csv: bool):
    """
    Perform the database rebuild. Optionally export CSV files first.
    """

    mode_text = 'with CSV export' if export_csv else 'no CSV export'
    print(f'Starting database rebuild process ({mode_text})...')
    print('=' * 60)

    try:
        step = 1

        if export_csv:
            print(f"\nStep {step}: Preparing data files")
            print('-' * 30)
            export_sheets_to_csv()
            step += 1

        # Reset database
        print(f"\nStep {step}: Resetting database")
        print('-' * 30)
        print('Dropping existing tables...')
        Base.metadata.drop_all(bind=engine)
        print('Dropped all tables')
        print('Creating fresh tables...')
        Base.metadata.create_all(bind=engine)
        print('Created all tables')
        step += 1


        # Load base data (conditionally based on available CSVs)
        print("\nStep {step}: Loading base data")
        print("-" * 30)
        load_roles()
        load_users()
        load_event_types()
        load_data_types()
        load_categories()
        load_sub_categories()
        load_selections()
        load_activity_logs()
        load_countries()
        load_states()
        load_addresses()
        load_companies()
        load_company_users()
        load_buyers()
        load_sellers()
        load_dd_users()
        load_products()
        load_templates()
        load_offensive_words()
        load_blogs()
        load_orders()
        load_dataset_orders()
        load_dataset_order_deliveries()
        load_live_lead_orders()
        load_live_lead_delivery_schedules()
        load_live_lead_order_status_history()
        load_daily_lead_delivery_logs()
        load_reviews()
        load_transactions()
        load_disputes()
        load_buyer_reports()
        load_buyer_dispute_reports()
        load_buyer_purchase_activity_reports()
        load_buyer_review_activity_reports()
        load_buyer_purchase_breakdown_reports()
        load_seller_reports()
        load_seller_rating_reports()
        load_seller_dispute_reports()
        load_seller_dispute_breakdown_reports()
        load_seller_listing_reports()
        load_seller_product_performance_reports()
        load_top_credits_usage_reports()
        load_credit_purchased_reports()
        load_most_verified_reports()
        load_api_usage_reports()
        load_check_type_reports()
        load_revenue_trend_reports()
        load_dispute_insights_reports()
        load_top_dispute_reasons_reports()
        load_top_categories_by_purchase_reports()
        load_lead_delivery_trend_reports()
        load_stats_layouts()

        # Generate metadata
        print("\nStep {step}: Generating metadata tables")
        print("-" * 30)
        populate_metadata_tables()

        print("\n" + "=" * 60)
        print("Database rebuild completed successfully!")
        print("=" * 60)
    except Exception:
        # Do not print success banner if any exception occurs
        print("\n" + "=" * 60)
        print("Database rebuild failed.")
        print("=" * 60)
        # Re-raise to allow upstream handling/logging if desired
        raise


@cli.command()
def rebuild():
    """
    Rebuild the database with seed data without exporting CSV files.
    """

    run_rebuild(export_csv=False)


@cli.command(name='rebuild-with-export')
def rebuild_with_export():
    """
    Rebuild the database with seed data (only for models present in this app).
    """

    run_rebuild(export_csv=True)

if __name__ == '__main__':
    cli()
