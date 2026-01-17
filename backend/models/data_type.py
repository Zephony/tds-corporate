from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class DataType(CommonColumnsMixin, BaseModel):
    __tablename__ = 'data_types'

    name: Mapped[str] = mc(String(255), unique=True, nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Data type name (e.g., Consumer, Business)',
        'display_type': 'text',
        'is_visible': False,
        'is_editable': False,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })
    description: Mapped[str|None] = mc(String(500), nullable=True, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Data type description',
        'display_type': 'text',
        'is_visible': False,
        'is_editable': False,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })
    status: Mapped[str] = mc(String(50), default='active', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Data type status',
        'display_type': 'text',
        'is_visible': False,
        'is_editable': False,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })

    updateable_fields = [
        'name',
        'description',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'description',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'status',
    ]

    searchable_fields = [
        'name',
        'description',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'status',
    ]