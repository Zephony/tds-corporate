from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class BuyerDisputeReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'buyer_dispute_reports'

    _info = {
        'description': 'Buyer dispute reporting data for analytics',
        'type': 'report',
        'api': {
            'routes': [
                'get_all',
            ],
        },
    }

    # Buyer identification
    id_buyer: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_buyer',
        'display_name': 'Buyer ID',
        'description': 'Foreign key reference to the buyer user',
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
        'display_name': 'User Name',
        'description': 'Display name of the buyer',
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
        'description': 'Email address of the buyer',
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
        'description': 'Date when the buyer signed up',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Order statistics
    leads_orders: Mapped[int] = mc(Integer, default=0, info={
        'name': 'leads_orders',
        'display_name': 'Leads Orders',
        'description': 'Number of lead-based orders placed by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    product_orders: Mapped[int] = mc(Integer, default=0, info={
        'name': 'product_orders',
        'display_name': 'Product Orders',
        'description': 'Number of product orders placed by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Dispute statistics
    disputes: Mapped[int] = mc(Integer, default=0, info={
        'name': 'disputes',
        'display_name': 'Disputes',
        'description': 'Total number of disputes raised by the buyer',
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
        'description': 'Current status of the buyer',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'leads_orders',
        'product_orders',
        'disputes',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'leads_orders',
        'product_orders',
        'disputes',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'leads_orders',
        'product_orders',
        'disputes',
        'status',
    ]

    searchable_fields = [
        'id_buyer',
        'user_name',
        'user_email',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'leads_orders',
        'product_orders',
        'disputes',
        'status',
    ]
