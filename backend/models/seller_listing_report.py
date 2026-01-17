from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SellerListingReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'seller_listing_reports'

    _info = {
        'description': 'Seller listing performance reporting data for analytics',
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
    
    # Listing performance metrics
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
    
    live_leads: Mapped[int] = mc(Integer, default=0, info={
        'name': 'live_leads',
        'display_name': 'Live Leads',
        'description': 'Number of currently live lead listings',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    dataset: Mapped[int] = mc(Integer, default=0, info={
        'name': 'dataset',
        'display_name': 'Dataset',
        'description': 'Number of dataset listings',
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
    
    cap_hit_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'cap_hit_rate',
        'display_name': 'Cap Hit Rate',
        'description': 'Cap hit rate percentage (e.g., 72%)',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_uploaded_on: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'last_uploaded_on',
        'display_name': 'Last Uploaded on',
        'description': 'Date and time when the seller last uploaded a listing',
        'display_type': 'datetime',
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
        'live_leads',
        'dataset',
        'delivery_rate',
        'cap_hit_rate',
        'last_uploaded_on',
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
        'live_leads',
        'dataset',
        'delivery_rate',
        'cap_hit_rate',
        'last_uploaded_on',
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
        'live_leads',
        'dataset',
        'delivery_rate',
        'cap_hit_rate',
        'last_uploaded_on',
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
        'live_leads',
        'dataset',
        'delivery_rate',
        'cap_hit_rate',
        'last_uploaded_on',
        'status',
    ]
