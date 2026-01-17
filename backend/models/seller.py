
from datetime import datetime

from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Seller(CommonColumnsMixin, BaseModel):
    __tablename__ = 'sellers'

    id_company: Mapped[int] = mc(
        ForeignKey('companies.id', name='fk_sellers_companies'),
        nullable=False,
        info={
            'name': 'id_company',
            'display_name': 'Company',
            'description': 'FK to Company representing the seller organisation',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Primary Contact Name',
        'description': 'Primary seller contact full name',
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
        'display_name': 'Contact Email',
        'description': 'Primary seller contact email address',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    position: Mapped[str | None] = mc(String(100), info={
        'name': 'position',
        'display_name': 'Position',
        'description': 'Contact position within the seller organisation',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })

    user_status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'user_status',
        'display_name': 'User Status',
        'description': 'Status of the seller contact user profile',
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

    seller_status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'seller_status',
        'display_name': 'Seller Status',
        'description': 'Operational status of the seller account',
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
                {'value': 'SUSPENDED', 'label': 'Suspended'},
            ]
        },
    })

    total_listings: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_listings',
        'display_name': 'Total Listings',
        'description': 'Total number of active listings for this seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    total_sales: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_sales',
        'display_name': 'Total Sales',
        'description': 'Total number of sales completed by this seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    rating: Mapped[float | None] = mc(Numeric(3, 2), info={
        'name': 'rating',
        'display_name': 'Seller Rating',
        'description': 'Average rating for the seller',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
        'max_value': 5,
    })

    updateable_fields = [
        'id_company',
        'name',
        'email',
        'position',
        'user_status',
        'seller_status',
        'total_listings',
        'total_sales',
        'rating',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_company',
        'name',
        'email',
        'position',
        'user_status',
        'seller_status',
        'total_listings',
        'total_sales',
        'rating',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'user_status',
        'seller_status',
        'total_listings',
        'total_sales',
        'rating',
    ]

    searchable_fields = [
        'name',
        'email',
        'position',
    ]

    filterable_fields = [
        'id',
        'id_company',
        'user_status',
        'seller_status',
    ]
