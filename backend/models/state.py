from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class State(CommonColumnsMixin, BaseModel):
    __tablename__ = 'states'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'State Name',
        'description': 'The official name of the state/province/region',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    code: Mapped[str|None] = mc(String(10), info={
        'name': 'code',
        'display_name': 'State Code',
        'description': 'State/province code (e.g., CA, TX, ENG, SCT)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 10,
    })
    id_country: Mapped[int] = mc(nullable=False, info={
        'name': 'id_country',
        'display_name': 'Country',
        'description': 'FK to Country that this state belongs to',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'name',
        'code',
        'id_country',
    ]

    readable_fields = [
        'id',
        'created_at',
        'name',
        'code',
        'id_country',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'name',
        'code',
    ]

    searchable_fields = [
        'name',
        'code',
    ]

    filterable_fields = [
        'id',
        'name',
        'code',
        'id_country',
    ]
