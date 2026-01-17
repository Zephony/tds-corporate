from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Blog(CommonColumnsMixin, BaseModel):
    __tablename__ = 'blogs'

    title: Mapped[str] = mc(
        String(255),
        nullable=False,
        info={
            'name': 'title',
            'display_name': 'Title',
            'description': 'Public facing blog title',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'max_length': 255,
        },
    )

    id_category: Mapped[int | None] = mc(
        ForeignKey('categories.id', name='fk_blogs_category'),
        info={
            'name': 'id_category',
            'display_name': 'Category',
            'description': 'FK to the associated content category',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    publication_status: Mapped[str] = mc(
        String(20),
        default='PENDING',
        nullable=False,
        info={
            'name': 'publication_status',
            'display_name': 'Publication Status',
            'description': 'Whether the blog is published or pending review',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': 'PUBLISHED', 'label': 'Published'},
                    {'value': 'PENDING', 'label': 'Pending'},
                ]
            },
        },
    )

    blog_status: Mapped[str] = mc(
        String(20),
        default='ACTIVE',
        nullable=False,
        info={
            'name': 'blog_status',
            'display_name': 'Blog Status',
            'description': 'Lifecycle status used for internal management',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': 'ACTIVE', 'label': 'Active'},
                    {'value': 'ARCHIVED', 'label': 'Archived'},
                ]
            },
        },
    )

    id_user: Mapped[int | None] = mc(
        ForeignKey('users.id', name='fk_blogs_user'),
        info={
            'name': 'id_user',
            'display_name': 'Author',
            'description': 'FK to the authoring user',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'title',
        'id_category',
        'publication_status',
        'blog_status',
        'id_user',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'title',
        'id_category',
        'publication_status',
        'blog_status',
        'id_user',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'title',
        'id_category',
        'publication_status',
        'blog_status',
    ]

    searchable_fields = [
        'title',
        'id_category',
    ]

    filterable_fields = [
        'id',
        'publication_status',
        'blog_status',
        'id_category',
        'id_user',
    ]
