from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class BuyerPurchaseActivityReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'buyer_purchase_activity_reports'

    _info = {
        'description': 'Buyer purchase activity reporting data for analytics',
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
    
    # Time-based spending metrics
    last_7_days: Mapped[Numeric] = mc(Numeric(15, 2), default=0.00, info={
        'name': 'last_7_days',
        'display_name': 'Last 7 Days',
        'description': 'Total spending in the last 7 days',
        'display_type': 'currency',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_30_days: Mapped[Numeric] = mc(Numeric(15, 2), default=0.00, info={
        'name': 'last_30_days',
        'display_name': 'Last 30 Days',
        'description': 'Total spending in the last 30 days',
        'display_type': 'currency',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    total_ytd: Mapped[Numeric] = mc(Numeric(15, 2), default=0.00, info={
        'name': 'total_ytd',
        'display_name': 'Total YTD',
        'description': 'Total year-to-date spending',
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
        'last_7_days',
        'last_30_days',
        'total_ytd',
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
        'last_7_days',
        'last_30_days',
        'total_ytd',
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
        'last_7_days',
        'last_30_days',
        'total_ytd',
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
        'last_7_days',
        'last_30_days',
        'total_ytd',
        'status',
    ]
