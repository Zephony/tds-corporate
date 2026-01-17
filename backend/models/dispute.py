from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, Numeric, Integer, DateTime, ForeignKey
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Dispute(CommonColumnsMixin, BaseModel):
    __tablename__ = 'disputes'
    
    _info = {
        'description': 'Disputes table tracking buyer-seller conflicts and resolutions',
        'type': 'operational',
    }

    title: Mapped[str] = mc(String(500), nullable=False, info={
        'name': 'title',
        'display_name': 'Dispute Title',
        'description': 'Brief title describing the dispute',
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
        'description': 'Detailed description of the dispute',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Dispute categorization and reason
    dispute_reason: Mapped[str] = mc(String(200), nullable=False, info={
        'name': 'dispute_reason',
        'display_name': 'Dispute Reason',
        'description': 'Specific reason for the dispute (e.g., False or Misleading Information)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'FALSE_OR_MISLEADING_INFORMATION', 'label': 'False or Misleading Information'},
                {'value': 'NON_DELIVERY_OF_LEADS', 'label': 'Non-Delivery of leads'},
                {'value': 'BAD_CONTACT', 'label': 'Bad Contact'},
                {'value': 'PAYMENT_ISSUE', 'label': 'Payment Issue'},
                {'value': 'DATA_QUALITY_ISSUE', 'label': 'Data Quality Issue'},
                {'value': 'GDPR_COMPLIANCE_ISSUE', 'label': 'GDPR Compliance Issue'},
                {'value': 'OTHER', 'label': 'Other'}
            ]
        },
    })
    
    # Timing
    raised_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'raised_date',
        'display_name': 'Raised Date',
        'description': 'Date and time when the dispute was raised',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    resolution_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'resolution_date',
        'display_name': 'Resolution Date',
        'description': 'Date and time when the dispute was resolved',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Enhanced status tracking
    status: Mapped[str] = mc(String(20), default='IN_PROGRESS', info={
        'name': 'status',
        'display_name': 'Dispute Status',
        'description': 'Current status of the dispute',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'IN_PROGRESS', 'label': 'In Progress'},
                {'value': 'RESOLVED', 'label': 'Resolved'},
                {'value': 'REFUNDED', 'label': 'Refunded'},
                {'value': 'DISPUTED', 'label': 'Disputed'},
                {'value': 'ESCALATED', 'label': 'Escalated'},
                {'value': 'CLOSED', 'label': 'Closed'}
            ]
        },
    })
    
    priority: Mapped[str] = mc(String(20), default='MEDIUM', info={
        'name': 'priority',
        'display_name': 'Priority',
        'description': 'Priority level of the dispute',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'LOW', 'label': 'Low'},
                {'value': 'MEDIUM', 'label': 'Medium'},
                {'value': 'HIGH', 'label': 'High'},
                {'value': 'URGENT', 'label': 'Urgent'}
            ]
        },
    })
    
    # Financial impact
    disputed_amount: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'disputed_amount',
        'display_name': 'Disputed Amount',
        'description': 'Amount in dispute',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    refund_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'refund_amount',
        'display_name': 'Refund Amount',
        'description': 'Amount refunded to resolve the dispute',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 0,
    })
    
    compensation_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'compensation_amount',
        'display_name': 'Compensation Amount',
        'description': 'Additional compensation provided to resolve the dispute',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 0,
    })
    
    # Resolution details
    resolution_notes: Mapped[str|None] = mc(Text, info={
        'name': 'resolution_notes',
        'display_name': 'Resolution Notes',
        'description': 'Details about how the dispute was resolved',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Related entities (following id_* convention)
    id_order: Mapped[int|None] = mc(Integer, info={
        'name': 'id_order',
        'display_name': 'Related Order',
        'description': 'FK to Order that this dispute relates to',
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
        'display_name': 'Related Product',
        'description': 'FK to Product that this dispute relates to',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Company relationships (complainant and respondent)
    id_complainant_company: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_complainant_company',
        'display_name': 'Complainant Company',
        'description': 'FK to Company raising the dispute',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_respondent_company: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_respondent_company',
        'display_name': 'Respondent Company',
        'description': 'FK to Company being disputed against',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # User who raised the dispute
    id_complainant_user: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_complainant_user',
        'display_name': 'Complainant User',
        'description': 'FK to User who raised the dispute',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    id_buyer: Mapped[int | None] = mc(
        ForeignKey('buyers.id', name='fk_disputes_buyers'),
        nullable=True,
        info={
            'name': 'id_buyer',
            'display_name': 'Buyer',
            'description': 'FK to Buyer associated with the dispute',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    id_seller: Mapped[int | None] = mc(
        Integer,
        nullable=True,
        info={
            'name': 'id_seller',
            'display_name': 'Seller ID',
            'description': 'Identifier for the seller associated with the dispute',
            'display_type': 'integer',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'title',
        'description',
        'dispute_reason',
        'raised_date',
        'resolution_date',
        'status',
        'priority',
        'disputed_amount',
        'refund_amount',
        'compensation_amount',
        'resolution_notes',
        'id_order',
        'id_product',
        'id_complainant_company',
        'id_respondent_company',
        'id_complainant_user',
        'id_buyer',
        'id_seller',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'title',
        'description',
        'dispute_reason',
        'raised_date',
        'resolution_date',
        'status',
        'priority',
        'disputed_amount',
        'refund_amount',
        'compensation_amount',
        'resolution_notes',
        'id_order',
        'id_product',
        'id_complainant_company',
        'id_respondent_company',
        'id_complainant_user',
        'id_buyer',
        'id_seller',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'raised_date',
        'resolution_date',
        'status',
        'priority',
        'disputed_amount',
        'refund_amount',
        'compensation_amount',
        'id_buyer',
        'id_seller',
    ]

    searchable_fields = [
        'title',
        'description',
        'dispute_reason',
        'resolution_notes',
    ]

    filterable_fields = [
        'id',
        'dispute_reason',
        'raised_date',
        'resolution_date',
        'status',
        'priority',
        'id_order',
        'id_product',
        'id_complainant_company',
        'id_respondent_company',
        'id_complainant_user',
        'id_buyer',
        'id_seller',
    ]
