import json

from datetime import datetime, UTC
from sqlalchemy import or_, func, event, String, Integer
from sqlalchemy.orm import Session, aliased, declared_attr

from backend.database import Base
from backend.helpers import camel_case_to_words, to_snake_case, deep_merge_dicts


class BaseModel(Base):
    __abstract__ = True
    
    @declared_attr
    def __table_args__(cls):
        class_name = cls.__name__
        lower_case_words = camel_case_to_words(class_name).lower()
        snake_case_name = to_snake_case(class_name)
        info = {
            'token': to_snake_case(class_name),
            'name': class_name,
            'description': f'The table that stores {lower_case_words}',
            'type': 'normal',
            'can_login': False,
            'api': {
                'is_enabled': True,
                'class_name': class_name,
                'name': class_name,
                'singular': snake_case_name,
                'plural': f'{snake_case_name}s',
                'routes': [
                    'get_one',
                    'get_all',
                    'post',
                    'patch',
                    'delete',
                ],
                'route_class': f'{class_name}Routes',
                'action_class': f'{class_name}Actions',
            },
        }

        overrides = getattr(cls, '_info', None)
        if isinstance(overrides, dict):
            info = deep_merge_dicts(info, overrides)

        return { 'info': info }
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def to_dict(self, full=False):
        """
        Convert model instance to dictionary with readable fields
        
        Args:
            full (bool): If True, return all fields, otherwise return only
            readable fields. This is used internally like dumping the entire
            row data while creating an event.
        """

        result = {}

        if full:
            fields = [c.name for c in self.__table__.columns]
        else:
            fields = self.readable_fields

        for field in fields:
            value = getattr(self, field)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[field] = value
        return result

    def update(self, data):
        """
        Update model fields from a dictionary.
        
        Args:
            data (dict): Dictionary containing field names and values to update
            
        Raises:
            ValueError: If any field in data is not in updateable_fields
        """

        # Check for invalid fields
        invalid_fields = [field for field in data.keys() if field not in self.updateable_fields]
        if invalid_fields:
            raise ValueError(f"Cannot update fields: {', '.join(invalid_fields)}")
        
        # Update valid fields
        for field, value in data.items():
            setattr(self, field, value)


    @classmethod
    def get_items(
        cls,
        db_session: Session,
        id=None,
        sort_details=None,
        details=False,
        filters=None,
        raw_filters=None,
        q=None,
        joins=[],
        list_joins=[],
        secondary_models_map={},
        pagination={},
    ):
        """
        Get items with sorting, limiting, and filtering.
        
        Args:
            db_session (Session): SQLAlchemy session
            sort_by (str): Column name to sort by
            reverse (bool): If True, sort in descending order
            details (bool): If True, return list of dictionaries with readable fields
            filters (list): List of filter dictionaries with structure:
                {
                    'field': str,  # Column name
                    'model': Model,  # The model to filter on
                    'lesser_than': int/str,  # Optional, int for Integer fields, ISO format string for DateTime/Date
                    'greater_than': int/str,  # Optional, int for Integer fields, ISO format string for DateTime/Date
                    'equal_to': int/str,  # Optional, int for Integer fields, ISO format string for DateTime/Date
                    'contains': str  # Optional, for string fields, case-insensitive wildcard match
                }
            q (str): Optional search string to match across searchable string columns
            joins (list): List of join dictionaries with structure:
                {
                    'model': Model,  # The model to join with
                    'column': str,   # The column to join on
                    'as_': str       # The key to use in the response for the joined model's details
                }
            list_joins (list): List of join dictionaries with structure:
                {
                    'model': Model,  # The model to join with
                    'column': str,   # The column to join on
                    'as_': str,      # The key to use in the response for the joined model's details
                    'sort_by': str,  # Optional, column name to sort the joined items by
                    'reverse': bool, # Optional, if True, sort in descending order
                    'limit': int     # Optional, maximum number of joined items to return per main item
                }
            secondary_models_map (dict): A map of secondary model classes
                that are joined to the main model class, but needed for searching.
                e.g. { 'role_details': GlobalRole }
            
        Returns:
            list: List of model instances or dictionaries if details=True
        """

        start_time = datetime.now()

        query = db_session.query(cls)
        
        # Apply deleted_at filter
        query = query.filter(cls.deleted_at == None)

        # Apply joins if provided
        if joins:
            for join in joins:
                model = join['model']
                column = join['column']
                
                if 'on' in join:
                    query = query.outerjoin(
                        model,
                        join['on']
                    ).add_entity(model)
                else:
                    query = query.outerjoin(
                        model,
                        getattr(cls, column) == getattr(model, 'id'),
                    ).add_entity(model)

        if raw_filters:
            query = query.filter(*raw_filters)

        # Apply filters to the main model if provided
        # print('filters', filters)
        if not id and filters:
            for filter_dict in filters:
                field = filter_dict.get('field')
                
                column = getattr(filter_dict['model'], field)
                
                # Skip if column is not Integer, DateTime/Date, or String type
                if not isinstance(
                    column.type,
                    (Integer, datetime, String),
                ):
                    continue
                
                # Apply filters
                if 'lesser_than' in filter_dict:
                    value = filter_dict['lesser_than']
                    query = query.filter(column < value)
                if 'greater_than' in filter_dict:
                    value = filter_dict['greater_than']
                    query = query.filter(column > value)
                if 'equal_to' in filter_dict:
                    value = filter_dict['equal_to']
                    query = query.filter(column == value)
                if 'contains' in filter_dict and isinstance(column.type, String):
                    value = filter_dict['contains']
                    query = query.filter(column.ilike(f'%{value}%'))

        # Apply global search if provided
        if not id and q and q.strip():
            search_conditions = []
            for field_text in cls.searchable_fields:
                if '.' in field_text:
                    as_, field = field_text.split('.')
                    Model = secondary_models_map[as_]
                else:
                    Model = cls
                    field = field_text

                column = getattr(Model, field)
                if isinstance(column.type, String):
                    search_conditions.append(column.ilike(f'%{q}%'))
            
            if search_conditions:
                # Combine all conditions with OR
                query = query.filter(or_(*search_conditions))
        
        # Get the sort column and direction. Then the sorting will be
        # applied here once and then in in list joins. Because
        # without that, if sorting is specified via list_joins,
        # that is applied to the main items list as well.
        sort_column = None
        sort_column_reverse = False
        if not id and sort_details:
            SortFieldModel = sort_details['model']
            field = sort_details['field']
            sort_column_reverse = sort_details['reverse']

            # Get the column to sort by
            try:
                sort_column = getattr(SortFieldModel, field)
            except AttributeError:
                # Default to id if invalid
                sort_column = getattr(cls, 'id')
                sort_column_reverse = False

        if sort_column:
            # Apply sorting
            if sort_column_reverse:
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Used to be returned inside the pagination dict
        total_main_rows = query.count()

        if id:
            query = query.filter(cls.id == id)
        else:
            # Create subquery for limited main items if page_size is specified
            if pagination.get('page_size'):
                # Calculate offset from page number (page 1 = offset 0)
                page = pagination.get('page', 1)
                offset = (page - 1) * pagination['page_size']
                
                if joins:
                    # When joins are present, we need to create a subquery that only contains
                    # the main model's ID, then join back to the full query
                    main_ids_subquery = query.with_entities(cls.id).offset(offset).limit(
                        pagination['page_size']
                    ).subquery()
                    query = query.join(main_ids_subquery, cls.id == main_ids_subquery.c.id)
                else:
                    # When no joins, we can use the simpler approach
                    subquery = query.offset(offset).limit(pagination['page_size']).subquery()
                    query = db_session.query(cls).join(subquery, cls.id == subquery.c.id)

        if list_joins:
            list_join_aliases = []  # Track the aliases we create
            for join in list_joins:
                model = join['model']
                column = join['column']
                
                # Create a window function to number rows within each group
                order_by = None
                if 'sort_by' in join:
                    order_by = getattr(model, join['sort_by'])
                    if join.get('reverse', False):
                        order_by = order_by.desc()
                
                row_number = func.row_number().over(
                    partition_by=getattr(model, column),
                    order_by=order_by
                ).label('row_number')
                
                # Create a subquery with the row numbers
                subquery = db_session.query(
                    model,
                    row_number
                ).filter(
                    getattr(model, column) == getattr(cls, 'id')
                ).subquery()
                
                # Create an alias for the subquery
                join_model_alias = aliased(model, subquery)
                list_join_aliases.append(join_model_alias)  # Store the alias
                
                # Join with the main query, filtering for only the first x rows
                join_condition = getattr(join_model_alias, column) == getattr(cls, 'id')
                if 'limit' in join:
                    join_condition = join_condition & (subquery.c.row_number <= join['limit'])
                
                query = query.outerjoin(
                    join_model_alias,
                    join_condition
                ).add_entity(join_model_alias)

                for join_of_list_join in join.get('joins', []):
                    # print('join_of_list_join', join_of_list_join)
                    # break
                    model = aliased(join_of_list_join['model'])
                    column = join_of_list_join['column']
                    
                    # Create an alias for the join model
                    # join_of_list_join_alias = db_session.aliased(model)
                    
                    query = query.outerjoin(
                        model,
                        getattr(join_model_alias, column) == getattr(model, 'id')
                    ).add_entity(model)
            
        # Apply list_joins sorting if specified. This sorting applies only
        # within the list and is applied after the main sorting.
        if list_joins:
            for i, join in enumerate(list_joins):
                # Reapplying the sorting here because the earlier sorting
                # would have been applied only to the subquery at this point.
                if sort_column:
                    # Apply sorting
                    if sort_column_reverse:
                        query = query.order_by(sort_column.desc())
                    else:
                        query = query.order_by(sort_column.asc())

                if 'sort_by' in join:
                    # Use the stored alias
                    aliased_model = list_join_aliases[i]
                    sort_column = getattr(aliased_model, join['sort_by'])
                    if join.get('reverse', False):
                        query = query.order_by(sort_column.desc())
                    else:
                        query = query.order_by(sort_column.asc())

        # print('=+=+=+=+=+=+=')
        # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
        # print('=============')

        # Execute the query and measure performance
        items = query.all()
        # print('Items', items)
        execution_time = datetime.now() - start_time
        # print(f'Database query executed in {execution_time.total_seconds() * 1000:.0f} milliseconds')

        # print('Items', items)

        if details:
            # unique_main_items: {
            #     id: main_item
            # }
            
            # Mainly used for list joins because that's when the db
            # will return multiple rows for the same item due to left
            # outer joins
            unique_main_items = {}
            for item_or_tuple in items:
                if not joins and not list_joins:
                    item = item_or_tuple
                    unique_main_items[item.id] = item.to_dict()
                else:
                    main_item = item_or_tuple[0]
                    joined_items = item_or_tuple[1:(len(joins) + 1)]
                    list_joined_items = item_or_tuple[(len(joins) + 1):]

                    item_dict = main_item.to_dict()
                    if main_item.id not in unique_main_items:
                        unique_main_items[main_item.id] = item_dict

                    if joins:
                        for i, joined_model in enumerate(joins):
                            # Since the first item is the main item
                            joined_item = joined_items[i]
                            as_key = joined_model['as_']
                            joined_item_details = joined_item.to_dict() if joined_item else None
                            unique_main_items[main_item.id][as_key] = joined_item_details

                    if list_joins:
                        for i, list_join in enumerate(list_joins):
                            list_joined_item = list_joined_items[i]

                            as_key = list_join['as_']
                            if as_key not in unique_main_items[main_item.id]:
                                unique_main_items[main_item.id][as_key] = []

                            
                            if list_joined_item is not None:
                                list_joined_item_details = list_joined_item.to_dict()

                                # Getting the item that is joined with the item
                                # of the list join
                                joins_of_list_join = list_join.get('joins', [])
                                index = 1
                                for join_of_list_join in joins_of_list_join:
                                    joined_item_of_list_joined_item = list_joined_items[i + index]
                                    if joined_item_of_list_joined_item:
                                        joined_item_of_list_joined_item_details = joined_item_of_list_joined_item.to_dict()
                                    else:
                                        joined_item_of_list_joined_item_details = None

                                    list_joined_item_details[join_of_list_join['as_']] = joined_item_of_list_joined_item_details
                                    index += 1

                                unique_main_items[main_item.id][as_key].append(
                                    list_joined_item_details
                                )
                
            item_dicts = list(unique_main_items.values())
            if id:
                return item_dicts[0] if item_dicts else None
            if pagination:
                pagination['returned_items'] = len(item_dicts)
                pagination['total_items'] = total_main_rows
            return item_dicts, pagination

        if id:
            return items[0] if items else None
        return items


# TODO: Probably a good idea to manually set this for all model fields
# Automatically set default 'is_initializable' in column info across all models
@event.listens_for(BaseModel, 'mapper_configured', propagate=True)
def _set_default_is_initializable(mapper, cls):
    """
    Ensure every column has an 'is_initializable' flag in its info dict.
    - For audit/system-managed fields, default to False
    - Otherwise mirror 'is_editable' (True -> True, missing/False -> False)
    Does not override if the model explicitly sets the flag.
    """

    audit_fields = {
        'id',
        'created_at',
        'last_updated_at',
        'deleted_at',
    }

    # Some models may not have a table (abstract), guard anyway
    if not hasattr(cls, '__table__'):
        return

    for column in cls.__table__.columns:
        info = column.info
        if 'is_initializable' in info:
            continue
        if column.name in audit_fields:
            info['is_initializable'] = False
            continue
        info['is_initializable'] = bool(info.get('is_editable', False))

