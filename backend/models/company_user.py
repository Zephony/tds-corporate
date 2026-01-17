from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class CompanyUser(CommonColumnsMixin, BaseModel):
    __tablename__ = 'company_users'

    position: Mapped[str|None] = mc(String(100), info={
        'name': 'position',
        'display_name': 'Position',
        'description': 'User position/role within the company (e.g., Owner, Manager, Sales Rep)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    is_primary_contact: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_primary_contact',
        'display_name': 'Is Primary Contact',
        'description': 'Whether this user is the primary contact for the company',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'User status within this company',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'ACTIVE', 'label': 'Active'},
                {'value': 'INACTIVE', 'label': 'Inactive'}
            ]
        },
    })
    joined_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'joined_date',
        'display_name': 'Joined Date',
        'description': 'Date when the user joined this company',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_company: Mapped[int] = mc(nullable=False, info={
        'name': 'id_company',
        'display_name': 'Company',
        'description': 'FK to Company',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_user: Mapped[int] = mc(nullable=False, info={
        'name': 'id_user',
        'display_name': 'User',
        'description': 'FK to User',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'position',
        'is_primary_contact',
        'status',
        'joined_date',
        'id_company',
        'id_user',
    ]

    readable_fields = [
        'id',
        'created_at',
        'position',
        'is_primary_contact',
        'status',
        'joined_date',
        'id_company',
        'id_user',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'position',
        'is_primary_contact',
        'status',
        'joined_date',
    ]

    searchable_fields = [
        'position',
    ]

    filterable_fields = [
        'id',
        'position',
        'is_primary_contact',
        'status',
        'id_company',
        'id_user',
    ]
