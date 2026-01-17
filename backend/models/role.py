from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Role(CommonColumnsMixin, BaseModel):
    __tablename__ = 'roles'

    name: Mapped[str] = mc(String(255), unique=True, nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Role name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Name of the role',
    })
    permission_bit_sequence: Mapped[str] = mc(String(255), default='0', info={
        'name': 'permission_bit_sequence',
        'display_name': 'Permission Bits',
        'description': 'Bit sequence of permissions',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Aggregate permission bits',
    })

    updateable_fields = [
        'name',
        'permission_bit_sequence',
    ]

    readable_fields = [
        'id',
        'created_at',
        'name',
        'permission_bit_sequence',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'name',
    ]

    searchable_fields = [
        'name',
    ]

    filterable_fields = [
        'id',
        'name',
    ]
