from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric
from datetime import datetime, date

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class ApiUsageReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'api_usage_reports'

    _info = {
        'description': 'API usage reporting data showing user API call statistics and error tracking',
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
    
    # API usage metrics
    total_api_calls: Mapped[int] = mc(Integer, default=0, info={
        'name': 'total_api_calls',
        'display_name': 'Total API Calls',
        'description': 'Total number of API calls made by the user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    successful_calls: Mapped[int] = mc(Integer, default=0, info={
        'name': 'successful_calls',
        'display_name': 'Successful Calls',
        'description': 'Number of successful API calls',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    failed_calls: Mapped[int] = mc(Integer, default=0, info={
        'name': 'failed_calls',
        'display_name': 'Failed Calls',
        'description': 'Number of failed API calls',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    success_rate: Mapped[Numeric] = mc(Numeric(5, 2), default=0.00, info={
        'name': 'success_rate',
        'display_name': 'Success Rate(%)',
        'description': 'Percentage of successful API calls',
        'display_type': 'percentage',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    most_common_error: Mapped[str|None] = mc(String(500), info={
        'name': 'most_common_error',
        'display_name': 'Most Common Error',
        'description': 'The most frequently occurring error for this user (with count)',
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
        'total_api_calls',
        'successful_calls',
        'failed_calls',
        'success_rate',
        'most_common_error',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'total_api_calls',
        'successful_calls',
        'failed_calls',
        'success_rate',
        'most_common_error',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'total_api_calls',
        'successful_calls',
        'failed_calls',
        'success_rate',
        'most_common_error',
        'status',
    ]

    searchable_fields = [
        'id_user',
        'user_name',
        'user_email',
        'most_common_error',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'total_api_calls',
        'successful_calls',
        'failed_calls',
        'success_rate',
        'most_common_error',
        'status',
    ]
