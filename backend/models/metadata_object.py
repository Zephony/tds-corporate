from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum

from backend.database import Base
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class ObjectTypeEnum(Enum):
    TABLE = 'table'
    VIEW = 'view'
    CUSTOM = 'custom'


class MetadataObject(CommonColumnsMixin, BaseModel):
    __tablename__ = 'metadata_objects'

    # Basic object information
    token: Mapped[str] = mc(String(255), unique=True, nullable=False, info={
        'name': 'token',
        'display_name': 'Token',
        'description': 'The token of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The token of the metadata_object',
    })
    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'The name of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The name of the metadata_object',
    })
    description: Mapped[str|None] = mc(Text,     info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'The description of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The description of the metadata_object',
    })
    
    # Object type and configuration
    object_type: Mapped[str] = mc(String(50), default=ObjectTypeEnum.TABLE.value, info={
        'name': 'object_type',
        'display_name': 'Object Type',
        'description': 'The object type of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The object type of the metadata_object',
    })
    table_name: Mapped[str|None] = mc(String(255), info={
        'name': 'table_name',
        'display_name': 'Table Name',
        'description': 'The table name of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The table name of the metadata_object',
    })
    model_class: Mapped[str|None] = mc(String(255), info={
        'name': 'model_class',
        'display_name': 'Model Class',
        'description': 'The model class of the metadata_object',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The model class of the metadata_object',
    })
    
    # UI/API configuration
    is_active: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_active',
        'display_name': 'Is Active',
        'description': 'The is active of the metadata_object',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The is active of the metadata_object',
    })
    is_system: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_system',
        'display_name': 'Is System',
        'description': 'The is system of the metadata_object',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The is system of the metadata_object',
    })
    is_read_only: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_read_only',
        'display_name': 'Is Read Only',
        'description': 'The is read only of the metadata_object',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The is read only of the metadata_object',
    })
    can_login: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'can_login',
        'display_name': 'Can Login',
        'description': 'Whether this object/entity can log into the system',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Can this object/entity log into the system?',
    })
    
    # General configuration
    configuration: Mapped[dict] = mc(JSONB, default={}, info={
        'name': 'configuration',
        'display_name': 'Configuration',
        'description': 'The general configuration of the metadata_object',
        'display_type': 'json',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The general configuration of the metadata_object',
    })
    
    # API configuration
    api_configuration: Mapped[dict] = mc(JSONB, default={}, info={
        'name': 'api_configuration',
        'display_name': 'API Configuration',
        'description': 'The API configuration of the metadata_object',
        'display_type': 'json',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The API configuration of the metadata_object',
    })

    updateable_fields = [
        'token',
        'name',
        'description',
        'object_type',
        'table_name',
        'model_class',
        'is_active',
        'is_read_only',
        ]
    
    readable_fields = [
        'id',
        'created_at',
        'token',
        'name',
        'description',
        'object_type',
        'table_name',
        'model_class',
        'is_active',
        'is_system',
        'is_read_only',
        'configuration',
        ]
    
    sortable_fields = [
        'id',
        'created_at',
        'token',
        'name',
        'object_type',
        'is_active',
        ]
    
    searchable_fields = [
        'token',
        'name',
        'description',
        'table_name',
        'model_class',
        ]
    
    filterable_fields = [
        'id',
        'token',
        'name',
        'object_type',
        'is_active',
        'is_system',
        'is_read_only',
        'configuration',
        ]

    def __repr__(self):
        return f'<MetadataObject {self.name}>' 