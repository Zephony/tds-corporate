from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Boolean

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class User(CommonColumnsMixin, BaseModel):
    __tablename__ = 'users'

    _info = {
        'can_login': True,
    }

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'User name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    email: Mapped[str] = mc(String(255), unique=True, nullable=False, info={
        'name': 'email',
        'display_name': 'Email',
        'description': 'User email',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    password: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'password',
        'display_name': 'Password',
        'description': 'Hashed password',
        'display_type': 'password',
        'is_visible': False,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })
    status: Mapped[str] = mc(String(50), default='active', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Account status',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_role: Mapped[int|None] = mc(nullable=True, info={
        'name': 'id_role',
        'display_name': 'Role',
        'description': 'FK to Role',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    is_anonymous: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_anonymous',
        'display_name': 'Is Anonymous',
        'description': 'Anonymous user flag',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    is_customer: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_customer',
        'display_name': 'Is Customer',
        'description': 'Customer flag',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    anonymous_token: Mapped[str|None] = mc(String(255), info={
        'name': 'anonymous_token',
        'display_name': 'Anonymous Token',
        'description': 'Token used for anonymous users',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': True,
    })

    updateable_fields = [
        'name',
        'email',
        'password',
        'status',
        'id_role',
        'is_anonymous',
        'is_customer',
        'anonymous_token',
    ]

    readable_fields = [
        'id',
        'created_at',
        'name',
        'email',
        'status',
        'id_role',
        'is_anonymous',
        'is_customer',
        'anonymous_token',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'name',
        'email',
        'status',
    ]

    searchable_fields = [
        'name',
        'email',
    ]

    filterable_fields = [
        'id',
        'name',
        'email',
        'status',
        'id_role',
        'is_anonymous',
        'is_customer',
    ]
