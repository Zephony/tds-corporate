from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_reports'

    _info = {
        'description': 'Seller reporting data for analytics',
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
    
    # Seller performance metrics
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
    
    leads_sold: Mapped[int] = mc(Integer, default=0, info={
        'name': 'leads_sold',
        'display_name': 'Leads Sold',
        'description': 'Total number of leads sold by the seller',
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
    
    dispute_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'dispute_rate',
        'display_name': 'Dispute Rate',
        'description': 'Dispute rate percentage (e.g., 3.1%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    avg_cpl: Mapped[Numeric] = mc(Numeric(10, 2), default=0.00, info={
        'name': 'avg_cpl',
        'display_name': 'Avg CPL',
        'description': 'Average Cost Per Lead',
        'display_type': 'currency',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    total_sales: Mapped[Numeric] = mc(Numeric(15, 2), default=0.00, info={
        'name': 'total_sales',
        'display_name': 'Total Sales',
        'description': 'Total sales revenue generated by the seller',
        'display_type': 'currency',
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
        'leads_sold',
        'delivery_rate',
        'dispute_rate',
        'avg_cpl',
        'total_sales',
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
        'leads_sold',
        'delivery_rate',
        'dispute_rate',
        'avg_cpl',
        'total_sales',
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
        'leads_sold',
        'delivery_rate',
        'dispute_rate',
        'avg_cpl',
        'total_sales',
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
        'leads_sold',
        'delivery_rate',
        'dispute_rate',
        'avg_cpl',
        'total_sales',
        'status',
    ]
