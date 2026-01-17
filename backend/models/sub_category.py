from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class SubCategory(CommonColumnsMixin, BaseModel):
    __tablename__ = 'sub_categories'
    __table_args__ = (  # type: ignore[assignment]
        UniqueConstraint('name', 'id_category', name='uq_name_category'),
        {'info': {
            'token': 'sub_category',
            'name': 'SubCategory',
            'description': 'The table that stores sub categories',
            'type': 'normal',
            'can_login': False,
            'api': {
                'is_enabled': True,
                'class_name': 'SubCategory',
                'name': 'SubCategory',
                'singular': 'sub_category',
                'plural': 'sub_categories',
                'routes': [
                    'get_one',
                    'get_all',
                    'post',
                    'patch',
                    'delete',
                ],
                'route_class': 'SubCategoryRoutes',
                'action_class': 'SubCategoryActions',
            },
        }}
    )

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Name of the sub category',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
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
    status: Mapped[str] = mc(String(50), default='ACTIVE_STATUS', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Sub category status (active/inactive)',
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
        'description': 'Icon/image identifier reference for the sub category',
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
        'id_category',
        'id_data_type',
        'status',
        'id_icon',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'id_category',
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
        'id_category',
        'id_data_type',
        'status',
    ]
