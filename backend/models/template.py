from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Template(CommonColumnsMixin, BaseModel):
    __tablename__ = 'templates'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'Template display name for admin users',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    description: Mapped[str | None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Internal notes about audience or usage',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })

    channel: Mapped[str] = mc(String(10), nullable=False, info={
        'name': 'channel',
        'display_name': 'Channel',
        'description': 'Messaging channel this template targets',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'EMAIL', 'label': 'Email'},
                {'value': 'SMS', 'label': 'SMS'},
            ]
        },
    })

    status: Mapped[str] = mc(String(10), default='ACTIVE', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Whether the template is available for use',
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
                {'value': 'INACTIVE', 'label': 'Inactive'},
            ]
        },
    })

    subject: Mapped[str | None] = mc(String(255), info={
        'name': 'subject',
        'display_name': 'Subject',
        'description': 'Email subject line (ignored for SMS)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    body: Mapped[str] = mc(Text, nullable=False, info={
        'name': 'body',
        'display_name': 'Body',
        'description': 'Template body content',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })

    # Email-specific flags
    has_attachment: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'has_attachment',
        'display_name': 'Has Attachment',
        'description': 'Email template includes an attachment placeholder',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    agent_active: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'agent_active',
        'display_name': 'Agent Active',
        'description': 'Visible to agents when channel is email',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    client_view: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'client_view',
        'display_name': 'Client View',
        'description': 'Marks email template as client-facing',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    # SMS-specific metadata
    template_type: Mapped[str | None] = mc(String(50), info={
        'name': 'template_type',
        'display_name': 'Template Type',
        'description': 'SMS template category (transactional, marketing, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 50,
    })

    character_count: Mapped[int | None] = mc(Integer, info={
        'name': 'character_count',
        'display_name': 'Character Count',
        'description': 'Length of SMS body used for compliance checks',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    agent_send: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'agent_send',
        'display_name': 'Agent Send',
        'description': 'Allows agents to send SMS manually',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    marketing: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'marketing',
        'display_name': 'Marketing',
        'description': 'Flags SMS template as promotional',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    version: Mapped[int] = mc(Integer, default=1, nullable=False, info={
        'name': 'version',
        'display_name': 'Version',
        'description': 'Version counter for change tracking',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    last_published_at: Mapped[datetime | None] = mc(DateTime(timezone=True), info={
        'name': 'last_published_at',
        'display_name': 'Last Published At',
        'description': 'Timestamp when the template was last activated',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    id_created_by_user: Mapped[int] = mc(
        ForeignKey('users.id', name='fk_templates_users'),
        nullable=False,
        info={
            'name': 'id_created_by_user',
            'display_name': 'Created By',
            'description': 'User who created or last published the template',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'name',
        'description',
        'channel',
        'status',
        'subject',
        'body',
        'has_attachment',
        'agent_active',
        'client_view',
        'template_type',
        'character_count',
        'agent_send',
        'marketing',
        'version',
        'last_published_at',
        'id_created_by_user',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'description',
        'channel',
        'status',
        'subject',
        'body',
        'has_attachment',
        'agent_active',
        'client_view',
        'template_type',
        'character_count',
        'agent_send',
        'marketing',
        'version',
        'last_published_at',
        'id_created_by_user',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'channel',
        'status',
        'agent_active',
        'client_view',
        'agent_send',
        'marketing',
        'version',
        'last_published_at',
    ]

    searchable_fields = [
        'name',
        'description',
        'subject',
        'body',
        'template_type',
    ]

    filterable_fields = [
        'id',
        'channel',
        'status',
        'has_attachment',
        'agent_active',
        'client_view',
        'template_type',
        'agent_send',
        'marketing',
        'version',
        'last_published_at',
        'id_created_by_user',
    ]
