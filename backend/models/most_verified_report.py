from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime, Date
from datetime import datetime, date

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class MostVerifiedReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'most_verified_reports'

    _info = {
        'description': 'Most verified reporting data showing users with highest verification activity',
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
    
    # Verification metrics (ordered by importance for this report)
    total_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'total_checks',
        'display_name': 'Total Checks',
        'description': 'Total number of verification checks performed by the user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    dd_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'dd_checks',
        'display_name': 'DD Checks',
        'description': 'Number of Due Diligence checks performed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    kyc_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'kyc_checks',
        'display_name': 'KYC Checks',
        'description': 'Number of Know Your Customer checks performed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    dd_kyc_checks: Mapped[int] = mc(Integer, default=0, info={
        'name': 'dd_kyc_checks',
        'display_name': 'DD & KYC Checks',
        'description': 'Number of combined Due Diligence and KYC checks performed',
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
        'description': 'Total amount spent on credits for verification checks',
        'display_type': 'currency',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_check: Mapped[date|None] = mc(Date, info={
        'name': 'last_check',
        'display_name': 'Last Check',
        'description': 'Date of the most recent verification check',
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
        'total_checks',
        'dd_checks',
        'kyc_checks',
        'dd_kyc_checks',
        'spent_on_credits',
        'last_check',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'total_checks',
        'dd_checks',
        'kyc_checks',
        'dd_kyc_checks',
        'spent_on_credits',
        'last_check',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'user_name',
        'user_email',
        'total_checks',
        'dd_checks',
        'kyc_checks',
        'dd_kyc_checks',
        'spent_on_credits',
        'last_check',
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
        'total_checks',
        'dd_checks',
        'kyc_checks',
        'dd_kyc_checks',
        'spent_on_credits',
        'last_check',
        'status',
    ]
