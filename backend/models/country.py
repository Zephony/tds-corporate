from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Country(CommonColumnsMixin, BaseModel):
    __tablename__ = 'countries'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Country Name',
        'description': 'The official name of the country',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    code: Mapped[str] = mc(String(10), unique=True, nullable=False, info={
        'name': 'code',
        'display_name': 'Country Code',
        'description': 'ISO country code (e.g., GB, US, CA)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 10,
    })
    flag_emoji: Mapped[str|None] = mc(String(10), info={
        'name': 'flag_emoji',
        'display_name': 'Flag Emoji',
        'description': 'Unicode flag emoji for the country',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'max_length': 10,
    })
    id_icon: Mapped[int|None] = mc(nullable=True, info={
        'name': 'id_icon',
        'display_name': 'Flag Icon',
        'description': 'FK to icon/image for country flag',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'name',
        'code',
        'flag_emoji',
        'id_icon',
    ]

    readable_fields = [
        'id',
        'created_at',
        'name',
        'code',
        'flag_emoji',
        'id_icon',
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
        'id_icon',
    ]
