from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum

from backend.database import Base
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class FieldTypeEnum(Enum):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    DATE = 'date'
    DATETIME = 'datetime'
    JSON = 'json'
    TEXT = 'text'
    ENUM = 'enum'
    FOREIGN_KEY = 'foreign_key'
    CUSTOM = 'custom'


class FieldDisplayTypeEnum(Enum):
    TEXT = 'text'
    TEXTAREA = 'textarea'
    NUMBER = 'number'
    CHECKBOX = 'checkbox'
    SELECT = 'select'
    MULTISELECT = 'multiselect'
    DATE = 'date'
    DATETIME = 'datetime'
    PASSWORD = 'password'
    EMAIL = 'email'
    URL = 'url'
    PHONE = 'phone'
    CURRENCY = 'currency'
    PERCENTAGE = 'percentage'
    FILE = 'file'
    IMAGE = 'image'
    RICH_TEXT = 'rich_text'
    CODE = 'code'
    JSON_EDITOR = 'json_editor'


class MetadataFieldStatusEnum(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DEPRECATED = 'deprecated'


class MetadataField(CommonColumnsMixin, BaseModel):
    __tablename__ = 'metadata_fields'

    # Basic field information
    name: Mapped[str] = mc(String(255), info={
        'name': 'name',
        'display_name': 'Field Name',
        'description': 'The name of the metadata field',
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
        'help_text': 'The name of the metadata field',
    })
    display_name: Mapped[str] = mc(String(255), info={
        'name': 'display_name',
        'display_name': 'Display Name',
        'description': 'The display name for the field in the UI',
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
        'help_text': 'The display name for the field in the UI',
    })
    description: Mapped[str|None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Description of the metadata field',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {'rows': 3},
        'validation_rules': {},
        'help_text': 'Description of the metadata field',
    })
    
    # Field type and display
    field_type: Mapped[str] = mc(String(50), info={
        'name': 'field_type',
        'display_name': 'Field Type',
        'description': 'The data type of the field (string, integer, float, boolean, etc.)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 50,
        'display_settings': {'options': ['string', 'integer', 'float', 'boolean', 'date', 'datetime', 'json', 'text', 'enum', 'foreign_key', 'custom']},
        'validation_rules': {'enum': ['string', 'integer', 'float', 'boolean', 'date', 'datetime', 'json', 'text', 'enum', 'foreign_key', 'custom']},
        'help_text': 'The data type of the field (string, integer, float, boolean, etc.)',
    })
    display_type: Mapped[str] = mc(String(50), info={
        'name': 'display_type',
        'display_name': 'Display Type',
        'description': 'How the field should be displayed in the UI',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 50,
        'display_settings': {'options': ['text', 'textarea', 'number', 'checkbox', 'select', 'multiselect', 'date', 'datetime', 'password', 'email', 'url', 'phone', 'currency', 'percentage', 'file', 'image', 'rich_text', 'code', 'json_editor']},
        'validation_rules': {'enum': ['text', 'textarea', 'number', 'checkbox', 'select', 'multiselect', 'date', 'datetime', 'password', 'email', 'url', 'phone', 'currency', 'percentage', 'file', 'image', 'rich_text', 'code', 'json_editor']},
        'help_text': 'How the field should be displayed in the UI',
    })
    
    # Database column information
    column_name: Mapped[str|None] = mc(String(255), nullable=True, info={
        'name': 'column_name',
        'display_name': 'Column Name',
        'description': 'The actual database column name for this field',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The actual database column name for this field',
    })
    column_type: Mapped[str|None] = mc(String(100), nullable=True, info={
        'name': 'column_type',
        'display_name': 'Column Type',
        'description': 'The database column type (e.g., VARCHAR, INTEGER, etc.)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The database column type (e.g., VARCHAR, INTEGER, etc.)',
    })
    is_nullable: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_nullable',
        'display_name': 'Nullable',
        'description': 'Whether this field can have null values in the database',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can have null values in the database',
    })
    is_primary_key: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_primary_key',
        'display_name': 'Primary Key',
        'description': 'Whether this field is a primary key in the database',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': False,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field is a primary key in the database',
    })
    is_unique: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_unique',
        'display_name': 'Unique',
        'description': 'Whether this field has a unique constraint in the database',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field has a unique constraint in the database',
    })
    is_indexed: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_indexed',
        'display_name': 'Indexed',
        'description': 'Whether this field has a database index',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field has a database index',
    })
    
    # Field properties
    is_required: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_required',
        'display_name': 'Required',
        'description': 'Whether this field is required',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field is required',
    })
    is_visible: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_visible',
        'display_name': 'Visible',
        'description': 'Whether this field is visible in the UI',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field is visible in the UI',
    })
    is_initializable: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_initializable',
        'display_name': 'Initializable',
        'description': 'Whether this field can be set during object initialization',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can be set during item creation',
    })
    is_editable: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_editable',
        'display_name': 'Editable',
        'description': 'Whether this field can be edited',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can be edited',
    })
    is_searchable: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_searchable',
        'display_name': 'Searchable',
        'description': 'Whether this field can be searched',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can be searched',
    })
    is_sortable: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_sortable',
        'display_name': 'Sortable',
        'description': 'Whether this field can be sorted',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can be sorted',
    })
    is_filterable: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_filterable',
        'display_name': 'Filterable',
        'description': 'Whether this field can be filtered',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Whether this field can be filtered',
    })
    
    # Field constraints
    min_length: Mapped[int|None] = mc(Integer, nullable=True, info={
        'name': 'min_length',
        'display_name': 'Minimum Length',
        'description': 'The minimum length for string fields',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 0,
        'display_settings': {},
        'validation_rules': {'min': 0},
        'help_text': 'The minimum length for string fields',
    })
    max_length: Mapped[int|None] = mc(Integer, nullable=True, info={
        'name': 'max_length',
        'display_name': 'Maximum Length',
        'description': 'The maximum length for string fields',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 1,
        'display_settings': {},
        'validation_rules': {'min': 1},
        'help_text': 'The maximum length for string fields',
    })
    min_value: Mapped[int|None] = mc(Integer, nullable=True, info={
        'name': 'min_value',
        'display_name': 'Minimum Value',
        'description': 'The minimum value for numeric fields',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The minimum value for numeric fields',
    })
    max_value: Mapped[int|None] = mc(Integer, nullable=True, info={
        'name': 'max_value',
        'display_name': 'Maximum Value',
        'description': 'The maximum value for numeric fields',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'The maximum value for numeric fields',
    })
    
    # Field settings and validation
    default_value: Mapped[str|None] = mc(Text, info={
        'name': 'default_value',
        'display_name': 'Default Value',
        'description': 'The default value for this field',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {'rows': 2},
        'validation_rules': {},
        'help_text': 'The default value for this field',
    })
    validation_rules: Mapped[dict] = mc(JSONB, default={}, info={
        'name': 'validation_rules',
        'display_name': 'Validation Rules',
        'description': 'Validation rules for this field',
        'display_type': 'json',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Validation rules for this field',
    })
    display_settings: Mapped[dict] = mc(JSONB, default={}, info={
        'name': 'display_settings',
        'display_name': 'Display Settings',
        'description': 'Display settings for this field in the UI',
        'display_type': 'json',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {},
        'validation_rules': {},
        'help_text': 'Display settings for this field in the UI',
    })
    
    # Field status and ordering
    status: Mapped[str] = mc(String(20), default=MetadataFieldStatusEnum.ACTIVE.value, info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'The status of the field (active, inactive, deprecated)',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'min_length': 1,
        'max_length': 20,
        'display_settings': {'options': ['active', 'inactive', 'deprecated']},
        'validation_rules': {'enum': ['active', 'inactive', 'deprecated']},
        'help_text': 'The status of the field (active, inactive, deprecated)',
    })
    display_order: Mapped[int] = mc(Integer, default=0, info={
        'name': 'display_order',
        'display_name': 'Display Order',
        'description': 'The order in which this field should be displayed',
        'display_type': 'integer',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 0,
        'max_value': 1000,
        'display_settings': {},
        'validation_rules': {'min': 0, 'max': 1000},
        'help_text': 'The order in which this field should be displayed',
    })
    
    # Help and documentation
    help_text: Mapped[str|None] = mc(Text, info={
        'name': 'help_text',
        'display_name': 'Help Text',
        'description': 'Help text to display for this field',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'display_settings': {'rows': 3},
        'validation_rules': {},
        'help_text': 'Help text to display for this field',
    })
    
    # Foreign keys
    
    id_user_created: Mapped[int|None] = mc(Integer, ForeignKey('users.id', name='fk_metadata_fields_user_created'), nullable=True, info={
        'name': 'id_user_created',
        'display_name': 'Created By User ID',
        'description': 'The ID of the user who created this field',
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
        'help_text': 'The ID of the user who created this field',
    })
    id_metadata_object: Mapped[int] = mc(Integer, ForeignKey('metadata_objects.id', name='fk_metadata_fields_object'), nullable=False, info={
        'name': 'id_metadata_object',
        'display_name': 'Metadata Object ID',
        'description': 'The ID of the metadata object this field belongs to',
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
        'help_text': 'The ID of the metadata object this field belongs to',
    })

    updateable_fields = [
        'name', 'display_name', 'description', 'field_type', 'display_type',
        'column_name', 'column_type', 'is_nullable', 'is_primary_key', 'is_unique', 'is_indexed',
        'is_required', 'is_visible', 'is_editable', 'is_searchable', 'is_sortable',
        'is_filterable', 'min_length', 'max_length', 'min_value', 'max_value',
        'default_value', 'validation_rules', 'display_settings',
        'status', 'display_order', 'help_text', 'id_metadata_object'
    ]
    readable_fields = [
        'id', 'created_at', 'name', 'display_name', 'description', 'field_type',
        'display_type', 'column_name', 'column_type', 'is_nullable', 'is_primary_key', 'is_unique', 'is_indexed',
        'is_required', 'is_visible', 'is_editable', 'is_searchable',
        'is_sortable', 'is_filterable', 'min_length', 'max_length', 'min_value', 'max_value',
        'default_value', 'validation_rules', 'display_settings', 'status', 'display_order', 'help_text',
        'id_user_created', 'id_metadata_object'
    ]
    sortable_fields = [
        'id', 'created_at', 'name', 'display_name', 'field_type', 'display_type',
        'column_name', 'column_type', 'is_nullable', 'is_primary_key', 'is_unique', 'is_indexed',
        'is_required', 'is_visible', 'is_editable', 'is_searchable', 'is_sortable',
        'is_filterable', 'status', 'display_order'
    ]
    searchable_fields = [
        'name', 'display_name', 'description', 'column_name', 'help_text'
    ]
    filterable_fields = [
        'id', 'name', 'field_type', 'display_type', 'column_name', 'column_type', 
        'is_nullable', 'is_primary_key', 'is_unique', 'is_indexed',
        'is_required', 'is_visible', 'is_editable', 'is_searchable', 'is_sortable', 'is_filterable',
        'status', 'id_user_created', 'id_metadata_object'
    ]

    def __repr__(self):
        return f'<MetadataField {self.name}>'