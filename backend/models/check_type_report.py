from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric
from datetime import datetime, date

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class CheckTypeReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'check_type_reports'

    _info = {
        'description': 'Check type reporting data showing verification statistics by check type',
        'type': 'report',
        'api': {
            'routes': [
                'get_all',
            ],
        },
    }

    # Check type identification
    check_type: Mapped[str] = mc(String(100), nullable=False, info={
        'name': 'check_type',
        'display_name': 'Check Type',
        'description': 'Type of verification check (DD Check, KYC Check, DD & KYC Check)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Check statistics
    total_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'total_checks',
        'display_name': 'Total Checks',
        'description': 'Total number of checks performed for this type',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    successful_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'successful_checks',
        'display_name': 'Successful Checks',
        'description': 'Number of successful checks for this type',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    failed_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'failed_checks',
        'display_name': 'Failed Checks',
        'description': 'Number of failed checks for this type',
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
        'description': 'Percentage of successful checks for this type',
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
        'description': 'The most frequently occurring error for this check type (with count)',
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
        'description': 'Current status of the check type',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'check_type',
        'total_checks',
        'successful_checks',
        'failed_checks',
        'success_rate',
        'most_common_error',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'check_type',
        'total_checks',
        'successful_checks',
        'failed_checks',
        'success_rate',
        'most_common_error',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'check_type',
        'total_checks',
        'successful_checks',
        'failed_checks',
        'success_rate',
        'most_common_error',
        'status',
    ]

    searchable_fields = [
        'check_type',
        'most_common_error',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'check_type',
        'total_checks',
        'successful_checks',
        'failed_checks',
        'success_rate',
        'most_common_error',
        'status',
    ]
