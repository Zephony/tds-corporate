from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerProductPerformanceReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_product_performance_reports'

    _info = {
        'description': 'Seller product performance reporting data for analytics',
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
    
    # Product/Listing details
    product_listing: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'product_listing',
        'display_name': 'Product/Listing',
        'description': 'Name of the product or listing',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    listing_type: Mapped[str] = mc(String(50), nullable=False, info={
        'name': 'listing_type',
        'display_name': 'Type',
        'description': 'Type of listing (Live Leads, Dataset, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Performance metrics
    leads_sold: Mapped[int] = mc(Integer, default=0, info={
        'name': 'leads_sold',
        'display_name': 'Leads Sold',
        'description': 'Number of leads sold for this product',
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
        'display_name': 'Dispute Rate',
        'description': 'Dispute rate percentage for this product (e.g., 0.9%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    cap_hit_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'cap_hit_rate',
        'display_name': 'Cap Hit Rate',
        'description': 'Cap hit rate percentage for this product (e.g., 72%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    refund_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'refund_rate',
        'display_name': 'Refund Rate',
        'description': 'Refund rate percentage for this product (e.g., 1.2%)',
        'display_type': 'percentage',
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
        'description': 'Average rating for this product (e.g., 4.8)',
        'display_type': 'rating',
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
        'description': 'Current status of the product',
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
        'product_listing',
        'listing_type',
        'leads_sold',
        'dispute_rate',
        'cap_hit_rate',
        'refund_rate',
        'avg_rating',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'product_listing',
        'listing_type',
        'leads_sold',
        'dispute_rate',
        'cap_hit_rate',
        'refund_rate',
        'avg_rating',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'product_listing',
        'listing_type',
        'leads_sold',
        'dispute_rate',
        'cap_hit_rate',
        'refund_rate',
        'avg_rating',
        'status',
    ]

    searchable_fields = [
        'id_seller',
        'user_name',
        'user_email',
        'product_listing',
        'listing_type',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_seller',
        'user_name',
        'user_email',
        'product_listing',
        'listing_type',
        'leads_sold',
        'dispute_rate',
        'cap_hit_rate',
        'refund_rate',
        'avg_rating',
        'status',
    ]
