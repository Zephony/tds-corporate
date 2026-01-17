import json

from typing import Dict, Any, Type, Optional, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.models import MetadataObject, MetadataField


# Field definitions
ForeignKeyField = Field(..., gt=0, description='Foreign key ID',)


field_types = {
    'string': {
        'name': 'String',
        'description': 'VARCHAR and TEXT fields',
        'properties': {
            'min_length': {
                'description': 'Minimum length',
            },
            'max_length': {
                'description': 'Maximum length',
            },
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'integer': {
        'name': 'Integer',
        'description': 'INTEGER fields',
        'properties': {
            'min_value': {
                'description': 'Minimum value',
            },
            'max_value': {
                'description': 'Maximum value',
            },
        },
    },
    'float': {
        'name': 'Float',
        'description': 'FLOAT fields',
        'properties': {
            'min_value': {
                'description': 'Minimum value',
            },
            'max_value': {
                'description': 'Maximum value',
            },
        },
    },
    'boolean': {
        'name': 'Boolean',
        'description': 'BOOLEAN fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'date': {
        'name': 'Date',
        'description': 'DATE fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'datetime': {
        'name': 'Datetime',
        'description': 'DATETIME fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'json': {
        'name': 'JSON',
        'description': 'JSONB fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'enum': {
        'name': 'Enum',
        'description': 'ENUM fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
        },
    },
    'foreign_key': {
        'name': 'Foreign key',
        'description': 'Foreign key fields',
        'properties': {
            'default_value': {
                'description': 'Default value',
            },
            'foreign_key_object': {
                'description': 'Foreign key object',
            },
        },
    },
}

field_display_types = {
    'text': {
        'name': 'Text',
        'field_type': 'string',
        'description': 'Text input',
    },
    'textarea': {
        'name': 'Textarea',
        'field_type': 'string',
        'description': 'Textarea input',
    },
    'email': {
        'name': 'Email',
        'field_type': 'string',
        'description': 'Email input',
    },
    'password': {
        'name': 'Password',
        'field_type': 'string',
        'description': 'Password input',
    },
    'phone': {
        'name': 'Phone',
        'field_type': 'string',
        'description': 'Phone input',
    },
    'url': {
        'name': 'URL',
        'field_type': 'string',
        'description': 'URL input',
    },
    'select': {
        'name': 'Select',
        'field_type': 'enum',
        'description': 'Select input',
    },
    'radio': {
        'name': 'Radio',
        'field_type': 'enum',
        'description': 'Radio input',
    },
    'checkbox': {
        'name': 'Checkbox',
        'field_type': 'boolean',
        'description': 'Checkbox input',
    },
    'date': {
        'name': 'Date',
        'field_type': 'date',
        'description': 'Date input',
    },
    'datetime': {
        'name': 'Datetime',
        'field_type': 'datetime',
        'description': 'Datetime input',
    },
    'json': {
        'name': 'JSON',
        'field_type': 'json',
        'description': 'JSON input',
    },
}


def get_field_pydantic_type(field: MetadataField) -> Type:
    """
    Get the appropriate Python type for a field based on its
    configuration.
    """

    field_type = field.field_type
    
    if field_type == 'email':
        return EmailStr
    elif field_type == 'password':
        return str
    elif field_type == 'foreign_key':
        return int
    elif field_type == 'text':
        return str
    elif field_type == 'string':
        return str
    elif field_type == 'json':
        return dict
    elif field_type == 'integer':
        return int
    elif field_type == 'float':
        return float
    elif field_type == 'boolean':
        return bool
    elif field_type == 'date':
        return str
    elif field_type == 'datetime':
        return str
    else:
        return str


def create_field(field: MetadataField, model_type: Literal['create', 'update']) -> Field:
    """
    Create a Pydantic Field with appropriate validation based on
    field configuration.
    """

    field_type = field.field_type
    description = field.description
    
    # Base field arguments
    field_args = {
        'description': description,
    }
    
    # Add type-specific validation
    if field_type == 'text' or field_type == 'password':
        field_args['min_length'] = field.min_length
        field_args['max_length'] = field.max_length
    elif field_type == 'foreign_key':
        field_args['gt'] = 0
    
    # Make field optional for update requests
    if model_type == 'update':
        field_args['default'] = None
    
    return Field(**field_args)


def generate_pydantic_model(
    object: MetadataObject,
    fields: list[MetadataField],
    model_type: Literal['create', 'update'],
) -> Type[BaseModel]:
    """
    Generate a Pydantic model for creating or updating object items.
    """

    final_fields = []
    for field in fields:
        if model_type == 'create' and not field.is_initializable:
            # print('Skipping non-initializable field:', field.name)
            continue

        final_fields.append(field)

    # print('Generating model for:', object.name)
    # print('Object:', object)
    # print('Fields:', final_fields)
    # Build type annotations (used by Pydantic)
    fields_dict = {}
    for field in final_fields:
        # print('Adding field:', field.name)
        field_type = get_field_pydantic_type(field)
        fields_dict[field.name] = field_type
    
    # Generate realistic examples based on actual fields
    example_data = {}
    for field in final_fields:
        field_name = field.name
        field_type = field.field_type
        
        if field_type == 'text':
            if 'name' in field_name.lower():
                example_data[field_name] = 'Sample Name'
            elif 'description' in field_name.lower():
                example_data[field_name] = 'Sample description text'
            elif 'email' in field_name.lower():
                example_data[field_name] = 'user@example.com'
            elif 'password' in field_name.lower():
                example_data[field_name] = 'securepassword123'
            elif 'token' in field_name.lower():
                example_data[field_name] = 'sample_token'
            else:
                example_data[field_name] = 'Sample text'
        elif field_type == 'integer':
            if 'id_' in field_name.lower():
                example_data[field_name] = 1
            elif 'count' in field_name.lower() or 'quantity' in field_name.lower():
                example_data[field_name] = 42
            else:
                example_data[field_name] = 100
        elif field_type == 'float':
            if 'price' in field_name.lower() or 'cost' in field_name.lower():
                example_data[field_name] = 19.99
            elif 'percentage' in field_name.lower() or 'rate' in field_name.lower():
                example_data[field_name] = 5.5
            else:
                example_data[field_name] = 10.5
        elif field_type == 'boolean':
            example_data[field_name] = True
        elif field_type == 'date':
            example_data[field_name] = '2024-01-15'
        elif field_type == 'datetime':
            example_data[field_name] = '2024-01-15T10:30:00Z'
        elif field_type == 'json':
            example_data[field_name] = {'key': 'value'}
        elif field_type == 'foreign_key':
            example_data[field_name] = 1
        else:
            example_data[field_name] = 'Sample value'
    
    # Create the model with ConfigDict
    model_dict = {
        '__annotations__': fields_dict,
        'model_config': {
            'extra': 'forbid',
            'json_schema_extra': {
                'examples': [
                    example_data,
                ],
            },
        },
    }
    
    # Attach Field(...) definitions (constraints/defaults)
    for field in final_fields:
        model_dict[field.name] = create_field(field, model_type)
    
    return type(
        f'{object.name}CreateRequest',
        (BaseModel,),
        model_dict,
    )

