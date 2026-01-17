from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerRatingReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_rating_reports'

    _info = {
        'description': 'Seller rating reporting data for analytics',
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
    
    # Rating and listing metrics
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
    
    review_count: Mapped[int] = mc(Integer, default=0, info={
        'name': 'review_count',
        'display_name': 'Review Count',
        'description': 'Total number of reviews received by the seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    avg_rating: Mapped[Numeric] = mc(Numeric(3, 1), default=0.0, info={
        'name': 'avg_rating',
        'display_name': 'Avg Rating',
        'description': 'Average star rating received by the seller (e.g., 4.8)',
        'display_type': 'rating',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_reviewed_product: Mapped[str|None] = mc(String(255), info={
        'name': 'last_reviewed_product',
        'display_name': 'Last Reviewed Product',
        'description': 'Name of the most recently reviewed product by the seller',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
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
        'review_count',
        'avg_rating',
        'last_reviewed_product',
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
        'review_count',
        'avg_rating',
        'last_reviewed_product',
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
        'review_count',
        'avg_rating',
        'last_reviewed_product',
        'status',
    ]

    searchable_fields = [
        'id_seller',
        'user_name',
        'user_email',
        'last_reviewed_product',
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
        'review_count',
        'avg_rating',
        'last_reviewed_product',
        'status',
    ]
