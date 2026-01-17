from sqlalchemy import JSON, String, UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class StatsLayout(CommonColumnsMixin, BaseModel):
    __tablename__ = 'stats_layouts'
    __table_args__ = (  # type: ignore[assignment]
        UniqueConstraint('id_user', 'layout_key', name='uq_stats_layout_user_key'),
        {
            'info': {
                'token': 'stats_layout',
                'name': 'Stats Layout',
                'description': 'Stores user-specific ordering for dashboard statistic blocks',
                'type': 'normal',
                'can_login': False,
                'api': {
                    'is_enabled': True,
                    'class_name': 'StatsLayout',
                    'name': 'Stats Layout',
                    'singular': 'stats_layout',
                    'plural': 'stats_layouts',
                    'routes': [
                        'get_one',
                        'get_all',
                        'post',
                        'patch',
                        'delete',
                    ],
                    'route_class': 'StatsLayoutRoutes',
                    'action_class': 'StatsLayoutActions',
                },
            },
        },
    )

    id_user: Mapped[int] = mc(Integer, ForeignKey('users.id', name='fk_stats_layouts_users'), nullable=False, info={
        'name': 'id_user',
        'display_name': 'User ID',
        'description': 'Identifier of the user who owns the layout configuration',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'help_text': 'User the layout applies to',
    })

    layout_key: Mapped[str] = mc(String(100), nullable=False, info={
        'name': 'layout_key',
        'display_name': 'Layout Key',
        'description': 'Page or context identifier for the stats layout',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'help_text': 'Key that distinguishes different dashboard pages or contexts',
    })

    component_order: Mapped[list[str]] = mc(JSON, default=list, nullable=False, info={
        'name': 'component_order',
        'display_name': 'Component Order',
        'description': 'Ordered list of stat component identifiers to display',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'help_text': 'Array of component keys in the preferred display order',
    })

    updateable_fields = [
        'layout_key',
        'component_order',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'layout_key',
        'component_order',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'layout_key',
    ]

    searchable_fields = [
        'layout_key',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_user',
        'layout_key',
    ]
