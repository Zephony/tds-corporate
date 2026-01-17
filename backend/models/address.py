from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Address(CommonColumnsMixin, BaseModel):
    __tablename__ = 'addresses'

    street_address: Mapped[str] = mc(String(500), nullable=False, info={
        'name': 'street_address',
        'display_name': 'Street Address',
        'description': 'The street address including building number and street name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 500,
    })
    address_line_2: Mapped[str|None] = mc(String(255), info={
        'name': 'address_line_2',
        'display_name': 'Address Line 2',
        'description': 'Additional address information (apartment, suite, unit, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'max_length': 255,
    })
    city: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'city',
        'display_name': 'City',
        'description': 'The city or town name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    postal_code: Mapped[str] = mc(String(20), nullable=False, info={
        'name': 'postal_code',
        'display_name': 'Postal Code',
        'description': 'ZIP code, postal code, or postcode',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 20,
    })
    id_country: Mapped[int] = mc(nullable=False, info={
        'name': 'id_country',
        'display_name': 'Country',
        'description': 'FK to Country for this address',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_state: Mapped[int|None] = mc(nullable=True, info={
        'name': 'id_state',
        'display_name': 'State/Province',
        'description': 'FK to State/Province (nullable for countries without states)',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'street_address',
        'address_line_2',
        'city',
        'postal_code',
        'id_country',
        'id_state',
    ]

    readable_fields = [
        'id',
        'created_at',
        'street_address',
        'address_line_2',
        'city',
        'postal_code',
        'id_country',
        'id_state',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'street_address',
        'city',
        'postal_code',
    ]

    searchable_fields = [
        'street_address',
        'address_line_2',
        'city',
        'postal_code',
    ]

    filterable_fields = [
        'id',
        'city',
        'postal_code',
        'id_country',
        'id_state',
    ]
