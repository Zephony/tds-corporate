from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, JSON, Integer, ForeignKey

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class ActivityLog(CommonColumnsMixin, BaseModel):
    __tablename__ = 'activity_logs'

    activity_type: Mapped[str] = mc(String(100), nullable=False, info={
        'name': 'activity_type',
        'display_name': 'Activity Type',
        'description': 'Type of activity (e.g., registration, purchase, dispute)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    # Activity categorization for buyer flow
    activity_category: Mapped[str] = mc(String(50), info={
        'name': 'activity_category',
        'display_name': 'Activity Category',
        'description': 'Category of buyer-related activity',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'REGISTRATION', 'label': 'Registration'},
                {'value': 'VERIFICATION', 'label': 'Verification'},
                {'value': 'APPROVAL', 'label': 'Approval'},
                {'value': 'PURCHASE', 'label': 'Purchase'},
                {'value': 'DISPUTE', 'label': 'Dispute'},
                {'value': 'PAYMENT', 'label': 'Payment'},
                {'value': 'SYSTEM', 'label': 'System'},
                {'value': 'GDPR', 'label': 'GDPR'}
            ]
        },
    })
    
    title: Mapped[str] = mc(String(500), nullable=False, info={
        'name': 'title',
        'display_name': 'Activity Title',
        'description': 'Human-readable title/summary of the activity',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 500,
    })
    
    description: Mapped[str|None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Detailed description of what happened',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Related entities (following id_* convention)
    id_user: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_user',
        'display_name': 'User',
        'description': 'FK to User who performed/triggered the activity',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_company: Mapped[int|None] = mc(Integer, info={
        'name': 'id_company',
        'display_name': 'Company',
        'description': 'FK to Company this activity relates to',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_order: Mapped[int|None] = mc(Integer, info={
        'name': 'id_order',
        'display_name': 'Order',
        'description': 'FK to Order for purchase-related activities',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_dispute: Mapped[int|None] = mc(Integer, info={
        'name': 'id_dispute',
        'display_name': 'Dispute',
        'description': 'FK to Dispute for dispute-related activities',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_product: Mapped[int|None] = mc(Integer, info={
        'name': 'id_product',
        'display_name': 'Product',
        'description': 'FK to Product for product-related activities',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_dd_user: Mapped[int|None] = mc(
        ForeignKey('dd_users.id', name='fk_activity_logs_dd_users'),
        nullable=True,
        info={
            'name': 'id_dd_user',
            'display_name': 'DD User',
            'description': 'FK to DD user associated with the activity',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )
    
    # Enhanced metadata for buyer activities
    activity_metadata: Mapped[dict|None] = mc(JSON, info={
        'name': 'activity_metadata',
        'display_name': 'Activity Metadata',
        'description': 'Additional structured data about the activity (amounts, references, etc.)',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'help_text': 'Store additional context like purchase amounts, product names, etc.'
    })

    updateable_fields = [
        'activity_type',
        'activity_category',
        'title',
        'description',
        'id_user',
        'id_company',
        'id_order',
        'id_dispute',
        'id_product',
        'id_dd_user',
        'activity_metadata',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'activity_type',
        'activity_category',
        'title',
        'description',
        'id_user',
        'id_company',
        'id_order',
        'id_dispute',
        'id_product',
        'id_dd_user',
        'activity_metadata',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'activity_type',
        'activity_category',
        'title',
        'id_user',
        'id_company',
        'id_dd_user',
    ]

    searchable_fields = [
        'activity_type',
        'activity_category',
        'title',
        'description',
    ]

    filterable_fields = [
        'id',
        'activity_type',
        'activity_category',
        'id_user',
        'id_company',
        'id_order',
        'id_dispute',
        'id_product',
        'id_dd_user',
    ]
