from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import DateTime

from backend.database import db


class CommonColumnsMixin:
    """Mixin providing common columns for all models."""
    
    id: Mapped[int] = mc(primary_key=True, sort_order=-1, info={
        'name': 'id',
        'display_name': 'ID',
        'description': 'The unique identifier for the item',
        'display_type': 'integer',
        'is_visible': True,
        'is_initializable': False,
        'is_editable': False,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The unique identifier for the item',
    })
    created_at: Mapped[datetime] = mc(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
        info={
            'name': 'created_at',
            'display_name': 'Created At',
            'description': 'The date and time the item was created',
            'display_type': 'datetime',
            'is_visible': True,
            'is_initializable': False,
            'is_editable': False,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {},
            'validation_rules': {},
            'help_text': 'The date and time the item was created',
        }
    )
    last_updated_at: Mapped[datetime|None] = mc(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(),
        info={
            'name': 'last_updated_at',
            'display_name': 'Last Updated At',
            'description': 'The date and time the item was last updated',
            'display_type': 'datetime',
            'is_visible': True,
            'is_initializable': False,
            'is_editable': False,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {},
            'validation_rules': {},
            'help_text': 'The date and time the item was last updated',
        }
    )
    deleted_at: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'deleted_at',
        'display_name': 'Deleted At',
        'description': 'The date and time the item was deleted',
        'display_type': 'datetime',
        'is_visible': True,
        'is_initializable': False,
        'is_editable': False,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The date and time the item was deleted',
    })
