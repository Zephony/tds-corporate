from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from enum import Enum

from backend.database import Base
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class RelationshipTypeEnum(Enum):
    ONE_TO_ONE = 'one_to_one'
    ONE_TO_MANY = 'one_to_many'
    MANY_TO_ONE = 'many_to_one'
    MANY_TO_MANY = 'many_to_many'


class RelationshipStatusEnum(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class MetadataRelationship(CommonColumnsMixin, BaseModel):
    __tablename__ = 'metadata_relationships'

    # Basic relationship information
    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Relationship Name',
        'description': 'The name of the metadata relationship',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 255,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The name of the metadata relationship',
    })
    display_name: Mapped[str] = mc(String(255), info={
        'name': 'display_name',
        'display_name': 'Display Name',
        'description': 'The display name for this relationship',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': False,
        'min_length': 1,
        'max_length': 255,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The display name for this relationship',
    })
    description: Mapped[str|None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Description of the metadata relationship',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {'rows': 3},
        'validation_rules': {},
        'help_text': 'Description of the metadata relationship',
    })
    
    # Relationship configuration
    relationship_type: Mapped[str] = mc(String(50), info={
        'name': 'relationship_type',
        'display_name': 'Relationship Type',
        'description': 'The type of relationship (one_to_one, one_to_many, many_to_one, many_to_many)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 50,
        'display_settings': {'options': ['one_to_one', 'one_to_many', 'many_to_one', 'many_to_many']},
        'validation_rules': {'enum': ['one_to_one', 'one_to_many', 'many_to_one', 'many_to_many']},
        'help_text': 'The type of relationship (one_to_one, one_to_many, many_to_one, many_to_many)',
    })
    status: Mapped[str] = mc(String(20), default=RelationshipStatusEnum.ACTIVE.value, info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'The status of the relationship (active or inactive)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 20,
        'display_settings': {'options': ['active', 'inactive']},
        'validation_rules': {'enum': ['active', 'inactive']},
        'help_text': 'The status of the relationship (active or inactive)',
    })
    
    # Source and target objects
    source_object_type: Mapped[str] = mc(String(100), info={
        'name': 'source_object_type',
        'display_name': 'Source Object Type',
        'description': 'The type of the source object in this relationship',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 100,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The type of the source object in this relationship',
    })
    target_object_type: Mapped[str] = mc(String(100), info={
        'name': 'target_object_type',
        'display_name': 'Target Object Type',
        'description': 'The type of the target object in this relationship',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 100,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The type of the target object in this relationship',
    })
    
    # Relationship properties
    is_required: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_required',
        'display_name': 'Required',
        'description': 'Whether this relationship is required',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this relationship is required',
    })
    is_cascading: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_cascading',
        'display_name': 'Cascading',
        'description': 'Whether changes cascade through this relationship',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether changes cascade through this relationship',
    })
    
    # Source and target metadata objects
    id_metadata_object_source: Mapped[int] = mc(Integer, ForeignKey('metadata_objects.id', name='fk_metadata_relationships_metadata_object_source'), nullable=False, info={
        'name': 'id_metadata_object_source',
        'display_name': 'Source Metadata Object ID',
        'description': 'The ID of the source metadata object in this relationship',
        'display_type': 'integer',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
        'max_value': 2147483647,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The ID of the source metadata object in this relationship',
    })
    id_metadata_object_target: Mapped[int] = mc(Integer, ForeignKey('metadata_objects.id', name='fk_metadata_relationships_metadata_object_target'), nullable=False, info={
        'name': 'id_metadata_object_target',
        'display_name': 'Target Metadata Object ID',
        'description': 'The ID of the target metadata object in this relationship',
        'display_type': 'integer',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
        'max_value': 2147483647,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The ID of the target metadata object in this relationship',
    })
    
    # Foreign keys
    
    id_user_created: Mapped[int|None] = mc(Integer, ForeignKey('users.id', name='fk_metadata_relationships_user_created'), nullable=True, info={
        'name': 'id_user_created',
        'display_name': 'Created By User ID',
        'description': 'The ID of the user who created this relationship',
        'display_type': 'integer',
        'is_visible': True,
        'is_editable': False,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
        'max_value': 2147483647,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The ID of the user who created this relationship',
    })

    updateable_fields = [
        'name', 'display_name', 'description', 'relationship_type', 'status',
        'source_object_type', 'target_object_type', 'is_required', 'is_cascading',
        'id_metadata_object_source', 'id_metadata_object_target'
    ]
    readable_fields = [
        'id', 'created_at', 'name', 'display_name', 'description', 'relationship_type',
        'status', 'source_object_type', 'target_object_type', 'is_required',
        'is_cascading', 'id_metadata_object_source', 'id_metadata_object_target', 
        'id_user_created'
    ]
    sortable_fields = [
        'id', 'created_at', 'name', 'display_name', 'relationship_type', 'status',
        'source_object_type', 'target_object_type', 'is_required', 'is_cascading',
        'id_metadata_object_source', 'id_metadata_object_target'
    ]
    searchable_fields = [
        'name', 'display_name', 'description', 'source_object_type', 'target_object_type'
    ]
    filterable_fields = [
        'id', 'name', 'relationship_type', 'status', 'source_object_type',
        'target_object_type', 'is_required', 'is_cascading', 
        'id_metadata_object_source', 'id_metadata_object_target',
        'id_user_created'
    ]

    def __repr__(self):
        return f'<MetadataRelationship {self.name}>'
