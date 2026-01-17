from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, Numeric, Integer, Boolean, DateTime, JSON, ForeignKey

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Product(CommonColumnsMixin, BaseModel):
    __tablename__ = 'products'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Product Name',
        'description': 'The name of the product/data listing',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    
    description: Mapped[str|None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Detailed description of the product/data listing',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Product Type - differentiates between live leads and data bundles
    product_type: Mapped[str] = mc(String(20), default='LIVE_LEADS', info={
        'name': 'product_type',
        'display_name': 'Product Type',
        'description': 'Type of product - live leads or data bundle',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'LIVE_LEADS', 'label': 'Live Leads'},
                {'value': 'DATA_BUNDLE', 'label': 'Data Bundle'}
            ]
        },
    })
    
    # Basic pricing - for simple fixed pricing
    price: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'price',
        'display_name': 'Base Price',
        'description': 'Base product price in the currency',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    # Tiered pricing system for quantity-based pricing
    pricing_tiers: Mapped[str|None] = mc(JSON, info={
        'name': 'pricing_tiers',
        'display_name': 'Pricing Tiers',
        'description': 'JSON array of quantity-based pricing options',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'help_text': 'Format: [{"quantity": 10000, "total_price": 1000, "price_per_lead": 0.10}]'
    })
    
    # Live leads specific fields
    daily_quantity: Mapped[int|None] = mc(Integer, info={
        'name': 'daily_quantity',
        'display_name': 'Daily Quantity',
        'description': 'Expected number of leads delivered per day (for live leads)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    minimum_quantity: Mapped[int|None] = mc(Integer, info={
        'name': 'minimum_quantity',
        'display_name': 'Minimum Quantity',
        'description': 'Minimum quantity that can be ordered',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
    })
    
    available_leads_next_7_days: Mapped[int|None] = mc(Integer, info={
        'name': 'available_leads_next_7_days',
        'display_name': 'Available Leads (Next 7 Days)',
        'description': 'Number of leads available for the next 7 days',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    lead_availability_schedule: Mapped[str|None] = mc(JSON, info={
        'name': 'lead_availability_schedule',
        'display_name': 'Lead Availability Schedule',
        'description': 'Weekly schedule showing lead availability by day',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'help_text': 'Format: {"sunday": {"time": "09:00 - 17:00", "available": 85}}'
    })
    
    # Data quantity and availability
    total_records: Mapped[int|None] = mc(Integer, info={
        'name': 'total_records',
        'display_name': 'Total Records',
        'description': 'Total number of data records available',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    available_records: Mapped[int|None] = mc(Integer, info={
        'name': 'available_records',
        'display_name': 'Available Records',
        'description': 'Number of records currently available for purchase',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    # Contact and delivery information
    contact_methods: Mapped[str|None] = mc(String(100), info={
        'name': 'contact_methods',
        'display_name': 'Contact Methods',
        'description': 'Available contact methods (Phone, Email, SMS)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    replacement_policy: Mapped[str|None] = mc(String(100), info={
        'name': 'replacement_policy',
        'display_name': 'Replacement Policy',
        'description': 'Policy for replacing invalid leads/data',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    data_source_name: Mapped[str|None] = mc(String(100), info={
        'name': 'data_source_name',
        'display_name': 'Data Source',
        'description': 'Source or origin of the data (Facebook, LinkedIn, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    # Duration and licensing
    listing_period_months: Mapped[int|None] = mc(Integer, info={
        'name': 'listing_period_months',
        'display_name': 'Listing Period (Months)',
        'description': 'How long the product listing is valid',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
        'max_value': 120,
    })
    
    license_period_months: Mapped[int|None] = mc(Integer, info={
        'name': 'license_period_months',
        'display_name': 'License Period (Months)',
        'description': 'How long the data license is valid',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
        'max_value': 120,
    })
    
    usage_limit_type: Mapped[str|None] = mc(String(50), info={
        'name': 'usage_limit_type',
        'display_name': 'Usage Limit Type',
        'description': 'Type of usage limitation (Unlimited, Single Use, etc.)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'UNLIMITED', 'label': 'Unlimited'},
                {'value': 'SINGLE_USE', 'label': 'Single Use'},
                {'value': 'LIMITED', 'label': 'Limited Use'},
                {'value': 'TIME_BASED', 'label': 'Time Based'}
            ]
        },
    })
    
    # Data types and sale types
    data_type: Mapped[str|None] = mc(String(50), info={
        'name': 'data_type',
        'display_name': 'Data Type',
        'description': 'Type of data (Consumer, Business, etc.)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'CONSUMER', 'label': 'Consumer'},
                {'value': 'BUSINESS', 'label': 'Business'},
                {'value': 'MIXED', 'label': 'Mixed'},
                {'value': 'OTHER', 'label': 'Other'}
            ]
        },
    })
    
    sale_type: Mapped[str|None] = mc(String(50), info={
        'name': 'sale_type',
        'display_name': 'Sale Type',
        'description': 'Type of sale (Full Sale, List Rental, etc.)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'FULL_SALE', 'label': 'Full Sale'},
                {'value': 'LIST_RENTAL', 'label': 'List Rental'},
                {'value': 'LICENSING', 'label': 'Licensing'},
                {'value': 'SUBSCRIPTION', 'label': 'Subscription'}
            ]
        },
    })
    
    # Geographic and demographic information
    geographic_coverage: Mapped[str|None] = mc(String(100), info={
        'name': 'geographic_coverage',
        'display_name': 'Geographic Coverage',
        'description': 'Geographic coverage area (Country Wide, Regional, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    restricted_use: Mapped[str|None] = mc(String(100), info={
        'name': 'restricted_use',
        'display_name': 'Restricted Use',
        'description': 'Any usage restrictions (Debt Management, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    # Source and validation information
    source_url: Mapped[str|None] = mc(String(500), info={
        'name': 'source_url',
        'display_name': 'Source URL',
        'description': 'URL of the data source or privacy policy',
        'display_type': 'url',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'max_length': 500,
    })
    
    uploaded_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'uploaded_date',
        'display_name': 'Uploaded Date',
        'description': 'When the data source was uploaded',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Validation status fields - Paper Trail tab
    tps_check_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'tps_check_status',
        'display_name': 'TPS Status',
        'description': 'Telephone Preference Service validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PASSED', 'label': 'Passed'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    mps_check_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'mps_check_status',
        'display_name': 'MPS Status',
        'description': 'Mail Preference Service validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PASSED', 'label': 'Passed'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    hlr_check_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'hlr_check_status',
        'display_name': 'HLR Check',
        'description': 'Home Location Register validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PASSED', 'label': 'Passed'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    llv_check_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'llv_check_status',
        'display_name': 'LLV Check',
        'description': 'Line Level Validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PASSED', 'label': 'Passed'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    geo_validation_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'geo_validation_status',
        'display_name': 'Geo Validation',
        'description': 'Geographic data validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'YES', 'label': 'Yes'},
                {'value': 'NO', 'label': 'No'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    suppression_check_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'suppression_check_status',
        'display_name': 'Suppression Check',
        'description': 'Suppression file validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'YES', 'label': 'Yes'},
                {'value': 'NO', 'label': 'No'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    gdpr_consent_status: Mapped[str|None] = mc(String(20), default='PENDING', info={
        'name': 'gdpr_consent_status',
        'display_name': 'GDPR Consent',
        'description': 'GDPR consent validation status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'YES', 'label': 'Yes'},
                {'value': 'NO', 'label': 'No'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'NOT_APPLICABLE', 'label': 'Not Applicable'}
            ]
        },
    })
    
    # Marketing metrics and engagement
    view_count: Mapped[int|None] = mc(Integer, default=0, info={
        'name': 'view_count',
        'display_name': 'View Count',
        'description': 'Number of times this product has been viewed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Should be updated programmatically
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    favorite_count: Mapped[int|None] = mc(Integer, default=0, info={
        'name': 'favorite_count',
        'display_name': 'Favorite Count',
        'description': 'Number of users who favorited this product',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Should be updated programmatically
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    rating_average: Mapped[float|None] = mc(Numeric(3, 2), info={
        'name': 'rating_average',
        'display_name': 'Average Rating',
        'description': 'Average user rating (0.00 - 5.00)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Should be calculated from ratings
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
        'max_value': 5,
    })
    
    # Product status
    status: Mapped[str] = mc(String(20), default='PENDING_APPROVAL', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Product approval/listing status',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'APPROVED', 'label': 'Approved'},
                {'value': 'REJECTED', 'label': 'Rejected'},
                {'value': 'PENDING_APPROVAL', 'label': 'Pending Approval'}
            ]
        },
    })
    
    # Foreign key relationships
    id_company: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_company',
        'display_name': 'Company',
        'description': 'FK to Company that owns this product',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    id_seller: Mapped[int | None] = mc(
        ForeignKey('sellers.id', name='fk_products_sellers'),
        nullable=True,
        info={
            'name': 'id_seller',
            'display_name': 'Seller',
            'description': 'FK to Seller responsible for this product',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )
    
    id_category: Mapped[int] = mc(
        ForeignKey('categories.id', name='fk_products_categories'),
        nullable=False,
        info={
        'name': 'id_category',
        'display_name': 'Category',
        'description': 'FK to Category for product classification',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_sub_category: Mapped[int] = mc(
        ForeignKey('sub_categories.id', name='fk_products_sub_categories'),
        nullable=False,
        info={
        'name': 'id_sub_category',
        'display_name': 'Sub Category',
        'description': 'FK to SubCategory for detailed classification',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_selection: Mapped[int] = mc(
        ForeignKey('selections.id', name='fk_products_selections'),
        nullable=False,
        info={
        'name': 'id_selection',
        'display_name': 'Selection',
        'description': 'FK to Selection for specific data type selection',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_created_by_user: Mapped[int] = mc(
        ForeignKey('users.id', name='fk_products_created_by_user'),
        nullable=False,
        info={
        'name': 'id_created_by_user',
        'display_name': 'Created By User',
        'description': 'FK to User who created this product',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': False,  # Should not be editable after creation
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    # Field access control
    updateable_fields = [
        'name',
        'description',
        'product_type',
        'price',
        'pricing_tiers',
        'daily_quantity',
        'minimum_quantity',
        'available_leads_next_7_days',
        'lead_availability_schedule',
        'total_records',
        'available_records',
        'contact_methods',
        'replacement_policy',
        'data_source_name',
        'listing_period_months',
        'license_period_months',
        'usage_limit_type',
        'data_type',
        'sale_type',
        'geographic_coverage',
        'restricted_use',
        'source_url',
        'uploaded_date',
        'tps_check_status',
        'mps_check_status',
        'hlr_check_status',
        'llv_check_status',
        'geo_validation_status',
        'suppression_check_status',
        'gdpr_consent_status',
        'status',
        'id_company',
        'id_category',
        'id_sub_category',
        'id_selection',
        'id_seller',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'description',
        'product_type',
        'price',
        'pricing_tiers',
        'daily_quantity',
        'minimum_quantity',
        'available_leads_next_7_days',
        'lead_availability_schedule',
        'total_records',
        'available_records',
        'contact_methods',
        'replacement_policy',
        'data_source_name',
        'listing_period_months',
        'license_period_months',
        'usage_limit_type',
        'data_type',
        'sale_type',
        'geographic_coverage',
        'restricted_use',
        'source_url',
        'uploaded_date',
        'tps_check_status',
        'mps_check_status',
        'hlr_check_status',
        'llv_check_status',
        'geo_validation_status',
        'suppression_check_status',
        'gdpr_consent_status',
        'view_count',
        'favorite_count',
        'rating_average',
        'status',
        'id_company',
        'id_category',
        'id_sub_category',
        'id_selection',
        'id_created_by_user',
        'id_seller',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'product_type',
        'price',
        'daily_quantity',
        'minimum_quantity',
        'total_records',
        'available_records',
        'listing_period_months',
        'license_period_months',
        'view_count',
        'favorite_count',
        'rating_average',
        'status',
        'id_seller',
    ]

    searchable_fields = [
        'name',
        'description',
        'contact_methods',
        'data_source_name',
        'geographic_coverage',
        'restricted_use',
    ]

    filterable_fields = [
        'id',
        'name',
        'product_type',
        'price',
        'daily_quantity',
        'minimum_quantity',
        'data_type',
        'sale_type',
        'usage_limit_type',
        'tps_check_status',
        'mps_check_status',
        'hlr_check_status',
        'llv_check_status',
        'geo_validation_status',
        'suppression_check_status',
        'gdpr_consent_status',
        'status',
        'id_company',
        'id_category',
        'id_sub_category',
        'id_selection',
        'id_created_by_user',
        'id_seller',
    ]
