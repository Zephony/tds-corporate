from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerDisputeReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_dispute_reports'

    _info = {
        'description': 'Seller dispute reporting data for analytics',
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
    
    # Basic metrics
    total_listing: Mapped[int] = mc(Integer, default=0, info={
        'name': 'total_listing',
        'display_name': 'Total Listing',
        'description': 'Total number of listings created by the seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    total_orders: Mapped[int] = mc(Integer, default=0, info={
        'name': 'total_orders',
        'display_name': 'Total Orders',
        'description': 'Total number of orders received by the seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    delivery_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'delivery_rate',
        'display_name': 'Delivery Rate',
        'description': 'Delivery rate percentage (e.g., 98.4%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Dispute-focused metrics
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
    
    dispute_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'dispute_rate',
        'display_name': 'Dispute Rate(%)',
        'description': 'Dispute rate percentage (e.g., 29.8%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    resolved_percentage: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'resolved_percentage',
        'display_name': 'Resolved (%)',
        'description': 'Dispute resolution rate percentage (e.g., 94%)',
        'display_type': 'percentage',
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
        'total_listing',
        'total_orders',
        'delivery_rate',
        'dispute_received',
        'dispute_rate',
        'resolved_percentage',
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
        'total_listing',
        'total_orders',
        'delivery_rate',
        'dispute_received',
        'dispute_rate',
        'resolved_percentage',
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
        'total_listing',
        'total_orders',
        'delivery_rate',
        'dispute_received',
        'dispute_rate',
        'resolved_percentage',
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
        'total_listing',
        'total_orders',
        'delivery_rate',
        'dispute_received',
        'dispute_rate',
        'resolved_percentage',
        'status',
    ]
