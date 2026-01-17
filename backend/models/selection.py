from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Selection(CommonColumnsMixin, BaseModel):
    __tablename__ = 'selections'
    __table_args__ = (  # type: ignore[assignment]
        UniqueConstraint('name', 'id_sub_category', name='uq_name_sub_category'),
        {'info': {
            'token': 'selection',
            'name': 'Selection',
            'description': 'The table that stores selections',
            'type': 'normal',
            'can_login': False,
            'api': {
                'is_enabled': True,
                'class_name': 'Selection',
                'name': 'Selection',
                'singular': 'selection',
                'plural': 'selections',
                'routes': [
                    'get_one',
                    'get_all',
                    'post',
                    'patch',
                    'delete',
                ],
                'route_class': 'SelectionRoutes',
                'action_class': 'SelectionActions',
            },
        }}
    )

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Selection Name',
        'description': 'Name of the selection',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_sub_category: Mapped[int] = mc(ForeignKey('sub_categories.id'), nullable=False, info={
        'name': 'id_sub_category',
        'display_name': 'Sub Category',
        'description': 'Foreign key reference to SubCategory model',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': True,
    })
    id_category: Mapped[int] = mc(ForeignKey('categories.id'), nullable=False, info={
        'name': 'id_category',
        'display_name': 'Category',
        'description': 'Foreign key reference to Category model',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
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
    selection_id: Mapped[str] = mc(String(100), unique=True, nullable=False, info={
        'name': 'selection_id',
        'display_name': 'Selection ID',
        'description': 'Unique identifier code for the selection (e.g., SLT46184137)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    status: Mapped[str] = mc(String(50), default='ACTIVE_STATUS', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Selection status (active/inactive)',
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
        'description': 'Icon/image identifier reference for the selection',
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
        'id_sub_category',
        'id_category',
        'id_data_type',
        'selection_id',
        'status',
        'id_icon',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'id_sub_category',
        'id_category',
        'id_data_type',
        'selection_id',
        'status',
        'id_icon',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'selection_id',
        'status',
    ]

    searchable_fields = [
        'name',
        'selection_id',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'id_sub_category',
        'id_category',
        'id_data_type',
        'selection_id',
        'status',
    ]
