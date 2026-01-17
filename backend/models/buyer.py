from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Buyer(CommonColumnsMixin, BaseModel):
    __tablename__ = 'buyers'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Primary buyer contact name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    email: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'email',
        'display_name': 'Email',
        'description': 'Primary buyer contact email',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    user_status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'user_status',
        'display_name': 'User Status',
        'description': 'Status of the buyer user profile',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'ACTIVE', 'label': 'Active'},
                {'value': 'INACTIVE', 'label': 'Inactive'},
            ]
        },
    })
    id_company: Mapped[int] = mc(ForeignKey('companies.id', name='fk_buyers_companies'), nullable=False, info={
        'name': 'id_company',
        'display_name': 'Company',
        'description': 'FK to Company representing the buyer organisation',
        'display_type': 'foreign_key',
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
        'description': 'Operational status of the buyer account',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'ACTIVE', 'label': 'Active'},
                {'value': 'INACTIVE', 'label': 'Inactive'},
            ]
        },
    })
    total_purchases: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_purchases',
        'display_name': 'Total Purchases',
        'description': 'Total number of purchases made by this buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    total_disputes: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_disputes',
        'display_name': 'Total Disputes',
        'description': 'Total disputes raised by this buyer (dummy value)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    first_purchase_date: Mapped[datetime | None] = mc(DateTime(timezone=True), info={
        'name': 'first_purchase_date',
        'display_name': 'First Purchase Date',
        'description': 'Timestamp of the buyer\'s first purchase',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    last_purchase_date: Mapped[datetime | None] = mc(DateTime(timezone=True), info={
        'name': 'last_purchase_date',
        'display_name': 'Last Purchase Date',
        'description': 'Timestamp of the buyer\'s most recent purchase',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    notes: Mapped[str | None] = mc(Text, info={
        'name': 'notes',
        'display_name': 'Internal Notes',
        'description': 'Free-form notes for CS or operations teams',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })

    updateable_fields = [
        'name',
        'email',
        'user_status',
        'id_company',
        'status',
        'total_purchases',
        'total_disputes',
        'first_purchase_date',
        'last_purchase_date',
        'notes',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'email',
        'user_status',
        'id_company',
        'status',
        'total_purchases',
        'total_disputes',
        'first_purchase_date',
        'last_purchase_date',
        'notes',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'status',
        'name',
        'email',
        'user_status',
        'total_purchases',
        'total_disputes',
        'first_purchase_date',
        'last_purchase_date',
    ]

    searchable_fields = [
        'notes',
    ]

    filterable_fields = [
        'id',
        'status',
        'user_status',
        'id_company',
    ]
