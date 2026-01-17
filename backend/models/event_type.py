from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class EventType(CommonColumnsMixin, BaseModel):
    __tablename__ = 'event_types'

    token: Mapped[str] = mc(String(255), unique=True, nullable=False, info={
        'name': 'token',
        'display_name': 'Token',
        'description': 'Event type token',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Event type name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    message: Mapped[str|None] = mc(Text, info={
        'name': 'message',
        'display_name': 'Message',
        'description': 'Default message for the event type',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    notes: Mapped[str|None] = mc(Text, info={
        'name': 'notes',
        'display_name': 'Notes',
        'description': 'Optional notes',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })

    updateable_fields = [
        'token',
        'name',
        'message',
        'notes',
    ]

    readable_fields = [
        'id',
        'created_at',
        'token',
        'name',
        'message',
        'notes',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'token',
        'name',
    ]

    searchable_fields = [
        'token',
        'name',
        'message',
        'notes',
    ]

    filterable_fields = [
        'id',
        'token',
        'name',
    ]
