import re
import copy
import json
import logging
import os
import jwt
import requests

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union, Tuple
from pydantic import ValidationError
from sqlalchemy import DateTime, String, Date


logger = logging.getLogger(__name__)


def unflatten_json(text):
    """
    Unflattens a flattened JSON string into a nested dictionary with type conversion.

    Examples:
        # Basic nested structure
        "a.b.c: 1, d.e.f: 2" -> {'a': {'b': {'c': 1}}, 'd': {'e': {'f': 2}}}
        
        # Boolean conversion
        "active: True, enabled: False" -> {'active': True, 'enabled': False}
        
        # Date normalization (various formats to yyyy-mm-dd)
        "created: 2024/01/15, updated: 2024-03-20" -> {'created': '2024-01-15', 'updated': '2024-03-20'}
        "start: 2024/1/5, end: 2024-12-25" -> {'start': '2024-01-05', 'end': '2024-12-25'}
        
        # Integer conversion
        "quantity: 42, count: 0" -> {'quantity': 42, 'count': 0}
        
        # Decimal conversion
        "price: 19.99, amount: 100.50" -> {'price': Decimal('19.99'), 'amount': Decimal('100.50')}
        "whole: 5.0" -> {'whole': 5}  # Whole decimals become integers
        
        # Quoted strings (preserved as strings)
        "name: 'John Doe', title: \"Manager\"" -> {'name': 'John Doe', 'title': 'Manager'}
        "id: '123', code: \"ABC\"" -> {'id': '123', 'code': 'ABC'}  # Quoted numbers stay strings
        
        # Mixed types
        "user.id: 123, user.name: 'John', user.active: True, user.created: 2024/01/15" ->
        {'user': {'id': 123, 'name': 'John', 'active': True, 'created': '2024-01-15'}}

    :param str text: The string to unflatten.

    :return dict: The unflattened dictionary with appropriate type conversions.
    """

    def convert_value(value_str):
        """Convert string value to appropriate type"""
        value_str = value_str.strip()
        
        # Check if value is quoted (preserve as string)
        if (value_str.startswith("'") and value_str.endswith("'")) or \
           (value_str.startswith('"') and value_str.endswith('"')):
            return value_str[1:-1]  # Remove quotes
        
        # Check for boolean values
        if value_str.lower() == 'true':
            return True
        elif value_str.lower() == 'false':
            return False
        
        # Check for date format (yyyy-mm-dd, yyyy/mm/dd, yyyy/m/d, etc.)
        date_patterns = [
            r'^\d{4}-\d{1,2}-\d{1,2}$',  # yyyy-mm-dd, yyyy-m-d
            r'^\d{4}/\d{1,2}/\d{1,2}$',  # yyyy/mm/dd, yyyy/m/d
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value_str):
                try:
                    # Try to parse the date
                    if '-' in value_str:
                        date_obj = datetime.strptime(value_str, '%Y-%m-%d')
                    else:
                        date_obj = datetime.strptime(value_str, '%Y/%m/%d')
                    # Normalize to yyyy-mm-dd format
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    # If date parsing fails, continue to other conversions
                    pass
        
        # Check for integer
        if value_str.isdigit():
            return int(value_str)
        
        # Check for decimal
        try:
            decimal_val = Decimal(value_str)
            # If it's a whole number, return as int
            if decimal_val == int(decimal_val):
                return int(decimal_val)
            return decimal_val
        except Exception:
            pass
        
        # Return as string if no conversion applies
        return value_str

    result = {}
    pairs = text.split(',')

    for pair in pairs:
        key, value = pair.split(':', 1)
        key = key.strip()
        value = convert_value(value)

        # Build nested keys
        parts = key.split('.')
        current = result
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value

    return result


def camel_case_to_words(text: str) -> str:
    """
    Convert CamelCase or PascalCase text to space-separated words.
    Example: "GlobalRole" -> "Global Role", "HTTPServerError" -> "HTTP Server Error".
    """
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2', text)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s1)


def to_snake_case(name: str) -> str:
    """
    Convert CamelCase/PascalCase to snake_case.
    Examples:
        'GlobalRoles' -> 'global_roles'
        'UserPermissions' -> 'user_permissions'
        'OrganizationTemplateRole' -> 'organization_template_role'
    """
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def deep_merge_dicts(base: Dict[str, Any], overrides: Dict[str, Any], *, copy_base: bool = True) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries. Values from overrides take precedence.
    - If both base[key] and overrides[key] are dicts, merge them recursively.
    - Otherwise, overrides[key] replaces base[key].
    Returns a new dict by default; set copy_base=False to merge into base.
    """
    result = copy.deepcopy(base) if copy_base else base
    for key, override_value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(override_value, dict):
            result[key] = deep_merge_dicts(result[key], override_value, copy_base=False)
        else:
            result[key] = override_value
    return result


def clean_gpt_response_text_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # inline code
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # links [text](url)
    text = re.sub(r'^#+\s*(.*)', r'\1', text, flags=re.MULTILINE)  # headings
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)   # bullet points
    return text.strip()


def send_email(
    to, subject, app_config, template_string,
    template=None, template_data=None, attachments=None,
    from_=None, reply_to=None, recipient_vars=None,
    delivery_time=None, attachment_files=[],
):
    """
    Takes care of sending an email based on the email service configured with
    the application.

    mailgun_config = {
        'sender': None,
        'url': None,
        'api_key': None,
    }

    `recipient_vars` is a must when sending bulk emails if you want to make
    sure it is sent individually to the recipients, otherwise they have
    the rest of the recipient addresses too.

    :param str template: The HTML email template file path
    :param dict template_data: The data to be rendered with the template
    :param list(str) to: List of recipients - Mailgun recipient format
    :param str subject: The email subject
    :param dict mailgun_config: Contains keys: `URL`, `API_KEY`, `SENDER`
    :param list(str) attachments: List of file paths to be attached
    :param ??? recipient_vars: ???
    :param datetime delivery_time: The time the email has to be delivered

    :return requests.models.Response:
    """

    if not app_config.get('MAILGUN'):
        print(f'Mailgun config is not present in environment: {app_config.get("APP_ENV")}')
        return None

    # Based on APP_ENV email is sent,
    # If APP_ENV is any of (None or local) => Email is not sent.
    # Else Email is sent to their respective email ID.
    if not app_config.get('APP_ENV') or app_config.get('APP_ENV', 'local') == 'local':
        print(f'Not sending email, local environment detected')
        return None
    else:
        print(f'Emailing {to}...')
        
    mailgun_config = app_config['MAILGUN']

    # logger.info(template_string)
    if template:
        # Note: render_template would need to be implemented for FastAPI
        # For now, just use template_string
        html = template_string
    else:
        html = template_string

    # logger.info(html)
    data = {
        'from': mailgun_config['SENDER'],
        'to': to,
        'subject': subject,
        'html': html,
    }

    if from_:
        data['from'] = from_

    if reply_to:
        data['h:Reply-To'] = reply_to

    if delivery_time:
        data['o:deliverytime'] = format_datetime(
            datetime.now(timezone.utc) + timedelta(days=int(delivery_time))
        )

    if recipient_vars:
        data['recipient-variables'] = recipient_vars

    files = []
    for attachment_file in attachment_files:
        file_ = (
            'attachment',
            (
                attachment_file['name'],
                open(attachment_file['path'], 'rb'),
                'application/pdf',
            ),
        )
        files.append(file_)

    # Requesting to Mailgun's REST API
    # Note that the mailgun config URL is different if Mailgun is
    # configured to send emails from the EU server rather than the US server
    import requests
    res = requests.post(
        mailgun_config['URL'],
        auth=('api', mailgun_config['API_KEY']),
        data=data,
        files=files,
    )

    return res


def parse_request_params(request_args, main_model_class, secondary_models_map={}):
    """
    Parse request parameters from request args.
    
    Args:
        request_args (dict): Request args dictionary
        main_model_class (class): The main model class to check column
            types and filterable fields
        secondary_models_map (dict): A map of secondary model classes
            that are joined to the main model class, but needed for filtering.
            e.g. { 'role_details': GlobalRole }
        
    Returns:
        (
            list: List of filter dictionaries
            str: The sort by column
            bool: To reverse sort the `sort_by` column or not
            str: Qstring search text
        )
    """

    # Column specific filters
    filters = []
    for param, value in request_args.items():
        if param.startswith('f_'):
            # field_path can be just the native field like 'id' or a joined field
            # like 'role_details.id'
            field_path = param[2:]  # Remove 'f_' prefix
            
            if '.' in field_path:
                as_, field = field_path.split('.')
                
                # Developer needs to pass this parameter in the route
                if as_ not in secondary_models_map:
                    continue

                # The model's filterable fields list should allow it
                if field_path not in main_model_class.filterable_fields:
                    continue
                
                model_class = secondary_models_map[as_]
            else:
                field = field_path
                model_class = main_model_class

            if field not in model_class.filterable_fields:
                continue
                
            # Get the column type
            column = getattr(model_class, field)
            column_type = column.type
            
            try:
                # Check if value starts with an operation
                if value.startswith('<'):
                    value_str = value[1:]
                    if isinstance(column_type, (DateTime, Date)):
                        try:
                            # Try parsing as date first
                            date_value = datetime.strptime(value_str, '%Y-%m-%d').date()
                            if isinstance(column_type, DateTime):
                                # For datetime fields, use start of day
                                value = datetime.combine(date_value, datetime.min.time())
                            else:
                                value = date_value
                        except ValueError:
                            # If not a date, try parsing as datetime
                            value = datetime.fromisoformat(value_str)
                    else:
                        value = int(value_str)
                    filters.append({
                        'model': model_class,
                        'field': field,
                        'lesser_than': value
                    })
                elif value.startswith('>'):
                    value_str = value[1:]
                    if isinstance(column_type, (DateTime, Date)):
                        try:
                            # Try parsing as date first
                            date_value = datetime.strptime(value_str, '%Y-%m-%d').date()
                            if isinstance(column_type, DateTime):
                                # For datetime fields, use end of day
                                value = datetime.combine(date_value, datetime.max.time())
                            else:
                                value = date_value
                        except ValueError:
                            # If not a date, try parsing as datetime
                            value = datetime.fromisoformat(value_str)
                    else:
                        value = int(value_str)
                    filters.append({
                        'model': model_class,
                        'field': field,
                        'greater_than': value
                    })
                elif value.startswith('~'):
                    # Wildcard match for string fields
                    if isinstance(column_type, String):
                        filters.append({
                            'model': model_class,
                            'field': field,
                            'contains': value[1:]  # Remove '~' prefix
                        })
                else:
                    # No operation specified, treat as equal_to
                    if isinstance(column_type, (DateTime, Date)):
                        try:
                            # Try parsing as date first
                            date_value = datetime.strptime(value, '%Y-%m-%d').date()
                            if isinstance(column_type, DateTime):
                                # For datetime fields, create a range for the entire day
                                filters.append({
                                    'model': model_class,
                                    'field': field,
                                    'greater_than': datetime.combine(date_value, datetime.min.time()),
                                    'lesser_than': datetime.combine(date_value, datetime.max.time())
                                })
                                continue
                            else:
                                value = date_value
                        except ValueError:
                            # If not a date, try parsing as datetime
                            value = datetime.fromisoformat(value)
                    elif isinstance(column_type, String):
                        # For string fields, treat as exact match
                        value = value
                    else:
                        value = int(value)
                    filters.append({
                        'model': model_class,
                        'field': field,
                        'equal_to': value
                    })
            except (ValueError, TypeError):
                continue  # Skip if value is not a valid integer or datetime

    # Sort column and order
    sort_details = None
    is_valid_sort_field = True
    sort_by_text = request_args.get('sort_by')
    if sort_by_text:
        if sort_by_text.startswith('-'):
            sort_reverse = True
        else:
            sort_reverse = False

        if '.' in sort_by_text:
            as_, field = sort_by_text.strip('-').split('.')
            if as_ not in secondary_models_map:
                is_valid_sort_field = False
            else:
                sort_field_model = secondary_models_map[as_]
        else:
            sort_field_model = main_model_class

        sort_field = sort_by_text.strip('-').split('.')[-1]

        if not is_valid_sort_field or sort_by_text.strip('-') not in main_model_class.sortable_fields:
            sort_details = {
                'model': main_model_class,
                'field': 'id',
                'reverse': False,
            }
        else:
            sort_details = {
                'model': sort_field_model,
                'field': sort_field,
                'reverse': sort_reverse,
            }

    # Get qsearch query
    q = request_args.get('q', None)

    # Pagination
    pagination = {}
    try:
        page = int(request_args.get('page', 1))
        pagination['page'] = page if page > 0 else 1
    except (ValueError, TypeError):
        pagination['page'] = 1
        
    try:
        page_size = int(request_args.get('page_size', 100))
        pagination['page_size'] = page_size if page_size > 0 else 100
    except (ValueError, TypeError):
        pagination['page_size'] = 100

    return {
        'filters': filters,
        'sort_details': sort_details,
        'q': q,
        'secondary_models_map': secondary_models_map,   # Used for searching in joined models
        'pagination': pagination,
    }


def responsify(data: Any, message: Optional[str] = None, status_code: int = 200) -> Dict[str, Any]:
    """
    Create a standardized API response similar to Flask backend.
    
    Args:
        data: Data dict/list or list of errors
        message: Optional message to be sent by the API
        status_code: The status code of the response
    
    Returns:
        dict: The standardized response dictionary
    """
    
    if status_code < 400:
        if isinstance(data, tuple):
            data, pagination = data
            return_dict = {
                'status': 'success',
                # 'status_code': status_code,
                'data': data,
                'message': message,
                'pagination': pagination,
            }
        else:
            return_dict = {
                'status': 'success',
                # 'status_code': status_code,
                'data': data,
                'message': message,
            }
        return return_dict

    return {
        'status': 'error',
        # 'status_code': status_code,
        'errors': data,
        'message': message,
    }


def decode_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT using SECRET_KEY; return claims or None if invalid/expired.
    """

    secret = os.getenv('SECRET_KEY')
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except Exception:
        return None


def _unused_create_error_response(
    message: str, 
    http_status: int = 400, 
    errors: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        http_status: HTTP status code
        errors: List of error dictionaries with 'field', 'description', and 'type' keys
    
    Returns:
        dict: Standardized error response
    """
    
    if errors is None:
        errors = []
    
    return {
        'status': 'error',
        'http_status': http_status,
        'errors': errors,
        'message': message,
    }


def validate_pydantic_errors(validation_error: ValidationError) -> List[Dict[str, str]]:
    """
    Convert Pydantic validation errors to the standard error format.
    
    Args:
        validation_error: Pydantic ValidationError
    
    Returns:
        list: List of error dictionaries with 'field', 'description', and 'type' keys
    """
    
    errors = []
    
    for error in validation_error.errors():
        # Convert location to field path (e.g., ['body', 'password'] -> 'body.password')
        field_parts = []
        for loc in error['loc']:
            if isinstance(loc, str):
                field_parts.append(loc)
            else:
                field_parts.append(str(loc))
        
        field = '.'.join(field_parts)
        description = error['msg']
        error_type = error.get('type', 'validation_error')
        
        errors.append({
            'field': field,
            'description': description,
            'type': error_type,
        })
    
    return errors


def _unused_create_validation_error_response(
    errors: List[Dict[str, str]], 
    message: str = "Validation failed"
) -> Dict[str, Any]:
    """
    Create a validation error response.
    
    Args:
        errors: List of error dictionaries with 'field' and 'description' keys
        message: Optional custom error message
    
    Returns:
        dict: Validation error response
    """
    
    return create_error_response(
        message=message,
        http_status=422,
        errors=errors,
    )


def send_websocket_task_update(task_id: int, status: str, message: str, data: Optional[Dict[str, Any]] = None):
    """
    Send a progress update to a specific task's WebSocket connection.
    This function can be called from Celery tasks to update frontend progress.
    
    Args:
        task_id: The ID of the task being processed
        status: Current status (e.g., 'processing', 'completed', 'failed')
        message: Human-readable message
        data: Optional additional data to include
    """

    try:
        progress_update = {
            "type": "task_progress",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        # Send the progress_update dict directly (no need to JSON encode it)
        # WebSocket endpoints are removed in minimal setup; this is a no-op
        return None
            
    except Exception as e:
        # Log error but don't fail the main task
        logger.error(f"Failed to send WebSocket progress update for task {task_id}: {e}")
