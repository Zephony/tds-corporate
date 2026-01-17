from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Boolean, DateTime, Integer
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class OffensiveWord(CommonColumnsMixin, BaseModel):
    __tablename__ = 'offensive_words'

    word: Mapped[str] = mc(String(100), nullable=False, unique=True, info={
        'name': 'word',
        'display_name': 'Offensive Word',
        'description': 'The offensive word or phrase to be filtered',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    
    severity: Mapped[str] = mc(String(20), default='MEDIUM', info={
        'name': 'severity',
        'display_name': 'Severity Level',
        'description': 'Severity level of the offensive word',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'LOW', 'label': 'Low'},
                {'value': 'MEDIUM', 'label': 'Medium'},
                {'value': 'HIGH', 'label': 'High'},
                {'value': 'CRITICAL', 'label': 'Critical'}
            ]
        },
    })
    
    is_active: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_active',
        'display_name': 'Active',
        'description': 'Whether this word is actively being filtered',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    added_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'added_date',
        'display_name': 'Added Date',
        'description': 'Date when this word was added to the filter list',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    usage_count: Mapped[int] = mc(Integer, default=0, info={
        'name': 'usage_count',
        'display_name': 'Usage Count',
        'description': 'Number of times this word was detected in reviews',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Should be updated programmatically
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    description: Mapped[str|None] = mc(String(255), info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Optional description or context for this word',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'max_length': 255,
    })
    
    # Relationships
    id_created_by_user: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_created_by_user',
        'display_name': 'Created By User',
        'description': 'FK to User who created this offensive word entry',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'word',
        'severity',
        'is_active',
        'added_date',
        'description',
        'id_created_by_user',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'word',
        'severity',
        'is_active',
        'added_date',
        'usage_count',
        'description',
        'id_created_by_user',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'word',
        'severity',
        'is_active',
        'added_date',
        'usage_count',
    ]

    searchable_fields = [
        'word',
        'description',
    ]

    filterable_fields = [
        'id',
        'word',
        'severity',
        'is_active',
        'added_date',
        'usage_count',
        'id_created_by_user',
    ]
