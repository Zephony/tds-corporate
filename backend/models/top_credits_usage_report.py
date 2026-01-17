from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime, Date
from datetime import datetime, date

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class TopCreditsUsageReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'top_credits_usage_reports'

    _info = {
        'description': 'Top credits usage reporting data for analytics',
        'type': 'report',
        'api': {
            'routes': [
                'get_all',
            ],
        },
    }

    # User identification
    id_user: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_user',
        'display_name': 'User ID',
        'description': 'Foreign key reference to the user',
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
        'description': 'Display name of the user',
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
        'description': 'Email address of the user',
        'display_type': 'email',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Credit usage metrics
    credit_used: Mapped[int] = mc(Integer, default=0, info={
        'name': 'credit_used',
        'display_name': 'Credit Used',
        'description': 'Total number of credits used by the user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    credit_purchased: Mapped[int] = mc(Integer, default=0, info={
        'name': 'credit_purchased',
        'display_name': 'Credit Purchased',
        'description': 'Total number of credits purchased by the user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    remaining_credits: Mapped[int] = mc(Integer, default=0, info={
        'name': 'remaining_credits',
        'display_name': 'Remaining Credits',
        'description': 'Number of credits remaining for the user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    spent_on_credits: Mapped[Numeric] = mc(Numeric(15, 2), default=0.00, info={
        'name': 'spent_on_credits',
        'display_name': 'Spent on Credits',
        'description': 'Total amount spent on purchasing credits',
        'display_type': 'currency',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_top_up: Mapped[date|None] = mc(Date, info={
        'name': 'last_top_up',
        'display_name': 'Last Top-up',
        'description': 'Date of the most recent credit top-up',
        'display_type': 'date',
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
        'description': 'Current status of the user',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'id_user',
        'user_name',
        'user_email',
        'credit_used',
        'credit_purchased',
        'remaining_credits',
        'spent_on_credits',
        'last_top_up',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'credit_used',
        'credit_purchased',
        'remaining_credits',
        'spent_on_credits',
        'last_top_up',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'credit_used',
        'credit_purchased',
        'remaining_credits',
        'spent_on_credits',
        'last_top_up',
        'status',
    ]

    searchable_fields = [
        'id_user',
        'user_name',
        'user_email',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'credit_used',
        'credit_purchased',
        'remaining_credits',
        'spent_on_credits',
        'last_top_up',
        'status',
    ]
