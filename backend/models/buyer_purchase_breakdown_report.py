from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class BuyerPurchaseBreakdownReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'buyer_purchase_breakdown_reports'

    _info = {
        'description': 'Buyer purchase breakdown reporting data for analytics',
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
    
    # Category-based purchase breakdown
    solar_leads: Mapped[int] = mc(Integer, default=0, info={
        'name': 'solar_leads',
        'display_name': 'Solar Leads',
        'description': 'Number of solar leads purchased by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    finance_leads: Mapped[int] = mc(Integer, default=0, info={
        'name': 'finance_leads',
        'display_name': 'Finance Leads',
        'description': 'Number of finance leads purchased by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    home_improvement: Mapped[int] = mc(Integer, default=0, info={
        'name': 'home_improvement',
        'display_name': 'Home Improvement',
        'description': 'Number of home improvement leads purchased by the buyer',
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
        'description': 'Number of other category leads purchased by the buyer',
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
        'solar_leads',
        'finance_leads',
        'home_improvement',
        'others',
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
        'solar_leads',
        'finance_leads',
        'home_improvement',
        'others',
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
        'solar_leads',
        'finance_leads',
        'home_improvement',
        'others',
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
        'solar_leads',
        'finance_leads',
        'home_improvement',
        'others',
        'status',
    ]
