from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Category(CommonColumnsMixin, BaseModel):
    __tablename__ = 'categories'
    __table_args__ = (  # type: ignore[assignment]
        UniqueConstraint('name', 'id_data_type', name='uq_name_data_type'),
        {'info': {
            'token': 'category',
            'name': 'Category',
            'description': 'The table that stores categories',
            'type': 'normal',
            'can_login': False,
            'api': {
                'is_enabled': True,
                'class_name': 'Category',
                'name': 'Category',
                'singular': 'category',
                'plural': 'categories',
                'routes': [
                    'get_one',
                    'get_all',
                    'post',
                    'patch',
                    'delete',
                ],
                'route_class': 'CategoryRoutes',
                'action_class': 'CategoryActions',
            },
        }}
    )

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Name of the category',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_data_type: Mapped[int] = mc(ForeignKey('data_types.id'), nullable=False, info={
        'name': 'id_data_type',
        'display_name': 'Data Type',
        'description': 'Foreign key reference to DataType model',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': True,
    })
    status: Mapped[str] = mc(String(50), default='active', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Category status (active/inactive)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_icon: Mapped[int|None] = mc(Integer, nullable=True, info={
        'name': 'id_icon',
        'display_name': 'Icon ID',
        'description': 'Icon/image identifier reference for the category',
        'display_type': 'integer',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })

    updateable_fields = [
        'name',
        'id_data_type',
        'status',
        'id_icon',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'id_data_type',
        'status',
        'id_icon',
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
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'id_data_type',
        'status',
    ]
