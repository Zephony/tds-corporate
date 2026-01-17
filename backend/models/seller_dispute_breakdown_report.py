from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerDisputeBreakdownReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_dispute_breakdown_reports'

    _info = {
        'description': 'Seller dispute breakdown by category reporting data for analytics',
        'type': 'report',
        'api': {
            'routes': [
                'get_all',
            ],
        },
    }

    # Seller identification
    id_seller: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_seller',
        'display_name': 'Seller ID',
        'description': 'Foreign key reference to the seller user',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    user_name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'user_name',
        'display_name': 'User',
        'description': 'Display name of the seller',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    user_email: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'user_email',
        'display_name': 'User Email',
        'description': 'Email address of the seller',
        'display_type': 'email',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    signed_up_date: Mapped[datetime] = mc(DateTime(timezone=True), nullable=False, info={
        'name': 'signed_up_date',
        'display_name': 'Signed Up Date',
        'description': 'Date when the seller signed up',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Dispute breakdown by category
    dispute_received: Mapped[int] = mc(Integer, default=0, info={
        'name': 'dispute_received',
        'display_name': 'Dispute Received',
        'description': 'Total number of disputes received by the seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    bad_contact: Mapped[int] = mc(Integer, default=0, info={
        'name': 'bad_contact',
        'display_name': 'Bad Contact',
        'description': 'Number of disputes due to bad contact data',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    invalid_data: Mapped[int] = mc(Integer, default=0, info={
        'name': 'invalid_data',
        'display_name': 'Invalid Data',
        'description': 'Number of disputes due to invalid data',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    criteria_mismatch: Mapped[int] = mc(Integer, default=0, info={
        'name': 'criteria_mismatch',
        'display_name': 'Criteria Mismatch',
        'description': 'Number of disputes due to criteria mismatch',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    others: Mapped[int] = mc(Integer, default=0, info={
        'name': 'others',
        'display_name': 'Others',
        'description': 'Number of disputes in other categories',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Status and metadata
    status: Mapped[str] = mc(String(50), default='ACTIVE_STATUS', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Current status of the seller',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'id_seller',
        'user_name',
        'user_email',
        'signed_up_date',
        'dispute_received',
        'bad_contact',
        'invalid_data',
        'criteria_mismatch',
        'others',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'signed_up_date',
        'dispute_received',
        'bad_contact',
        'invalid_data',
        'criteria_mismatch',
        'others',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'signed_up_date',
        'dispute_received',
        'bad_contact',
        'invalid_data',
        'criteria_mismatch',
        'others',
        'status',
    ]

    searchable_fields = [
        'id_seller',
        'user_name',
        'user_email',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'signed_up_date',
        'dispute_received',
        'bad_contact',
        'invalid_data',
        'criteria_mismatch',
        'others',
        'status',
    ]
