import os
import uuid
import bcrypt
import jwt
from datetime import datetime, UTC
from datetime import timedelta
from fastapi import (
    UploadFile,
    
    # Because there's a model called Request
    Request as FastAPIRequest,
)

from backend.database import Session
from backend.models import *
from backend.exceptions import (
    InvalidRequestData,
    ResourceNotFound,
    InternalServerError,
)
from backend.helpers import decode_jwt_token


def get_model_relationships(model_class, db_session):
    """
    Get relationships for a model based on metadata_relationships table.
    
    Args:
        model_class: The SQLAlchemy model class
        db_session: Database session
        
    Returns:
        dict: Dictionary with 'joins' and 'list_joins' lists containing relationship information
    """
    if not hasattr(model_class, '__name__'):
        return {'joins': [], 'list_joins': []}
    
    class_name = model_class.__name__
    
    # Query metadata relationships where this model is the source
    relationships = db_session.query(MetadataRelationship).filter(
        MetadataRelationship.source_object_type == class_name,
        MetadataRelationship.status == 'active'
    ).all()
    
    joins = []
    list_joins = []
    
    # Build model map dynamically from all imported models
    import sys
    current_module = sys.modules[__name__]
    model_map = {}
    
    # Get all classes from the current module that inherit from BaseModel
    for name in dir(current_module):
        obj = getattr(current_module, name)
        if (hasattr(obj, '__mro__') and 
            hasattr(obj, '__tablename__') and 
            BaseModel in obj.__mro__ and 
            obj != BaseModel
        ):
            model_map[obj.__name__] = obj
    
    for relationship in relationships:
        target_model_class = model_map.get(relationship.target_object_type)
        if not target_model_class:
            continue
            
        # Determine the foreign key column name (assuming naming convention id_{target_table})
        target_table_name = target_model_class.__tablename__
        api_config = getattr(target_model_class.__table__, 'info', {}).get('api', {})
        singular_name = api_config.get('singular')

        if not singular_name:
            if target_table_name.endswith('ies'):
                singular_name = f"{target_table_name[:-3]}y"
            elif target_table_name.endswith('ses'):
                singular_name = target_table_name[:-2]
            elif target_table_name.endswith('s'):
                singular_name = target_table_name[:-1]
            else:
                singular_name = target_table_name

        fk_column = f'id_{singular_name}'
        
        # Handle special cases for table names
        if target_table_name == 'data_types':
            fk_column = 'id_data_type'
        
        # Check if the foreign key column exists in the source model
        if hasattr(model_class, fk_column):
            join_config = {
                'model': target_model_class,
                'column': fk_column,
                'as_': f'{singular_name}_details',
            }
            
            # For many-to-one relationships, use regular joins
            # For one-to-many relationships, use list_joins
            if relationship.relationship_type == 'many_to_one':
                joins.append(join_config)
            elif relationship.relationship_type == 'one_to_many':
                # For one-to-many, we need to reverse the join logic
                # The foreign key would be in the target model pointing to this model
                reverse_fk_column = f'id_{model_class.__tablename__[:-1] if model_class.__tablename__.endswith("s") else model_class.__tablename__}'
                if hasattr(target_model_class, reverse_fk_column):
                    list_join_config = {
                        'model': target_model_class,
                        'column': reverse_fk_column,
                        'as_': f'{target_table_name}_details',
                        'sort_by': 'id',
                        'reverse': False,
                        'limit': 100,
                    }
                    list_joins.append(list_join_config)
    
    return {'joins': joins, 'list_joins': list_joins}


class BackgroundJobActions:
    @staticmethod
    def do_dummy_job(payload: dict):
        now = datetime.now(UTC)
        message = (payload or {}).get('message')
        return {
            'status': 'completed',
            'processed_at': now.isoformat(),
            'echo': message,
            'payload': payload,
        }


class DynamicActions:
    @staticmethod
    def get_one(model_class, id_item, db_session):
        # Get relationships for this model from metadata
        relationships = get_model_relationships(model_class, db_session)
        
        item = model_class.get_items(
            db_session=db_session,
            id=id_item,
            details=True,
            joins=relationships['joins'],
            list_joins=relationships['list_joins'],
        )
        if not item:
            raise ResourceNotFound(
                message=f"{model_class.__table__.info['name']} with ID {id_item} not found",
            )
        return item

    @staticmethod
    def get_all(
        model_class,
        db_session,
        filters,
        sort_details,
        q,
        secondary_models_map={},
        pagination={},
    ):
        # Get relationships for this model from metadata
        relationships = get_model_relationships(model_class, db_session)
        
        items, pagination = model_class.get_items(
            db_session=db_session,
            filters=filters,
            details=True,
            sort_details=sort_details,
            q=q,
            secondary_models_map=secondary_models_map,
            pagination=pagination,
            joins=relationships['joins'],
            list_joins=relationships['list_joins'],
        )
        return items, pagination

    @staticmethod
    def create(model_class, data, db_session):
        # Only allow columns marked as initializable during creation
        initializable_fields = [
            column.name
            for column in model_class.__table__.columns
            if column.info.get('is_initializable')
        ]

        invalid_fields = [field for field in data if field not in initializable_fields]
        if invalid_fields:
            raise InvalidRequestData(
                errors=[
                    {
                        'field': field,
                        'description': 'Field cannot be set during creation',
                    }
                    for field in invalid_fields
                ],
                message='Invalid fields in create request',
            )

        create_kwargs = {field: data[field] for field in initializable_fields if field in data}

        try:
            item = model_class(**create_kwargs)
        except TypeError as exc:
            raise InvalidRequestData(
                message='Invalid payload for create request',
                errors=[
                    {
                        'field': 'payload',
                        'description': str(exc),
                    }
                ],
            ) from exc

        db_session.add(item)
        db_session.flush()
        db_session.refresh(item)

        relationships = get_model_relationships(model_class, db_session)
        return model_class.get_items(
            db_session=db_session,
            id=item.id,
            details=True,
            joins=relationships['joins'],
            list_joins=relationships['list_joins'],
        )

    @staticmethod
    def update(model_class, data, db_session, **identifiers):
        if not identifiers:
            raise InvalidRequestData(
                message='Missing identifier for update request',
            )

        identifier_field, identifier_value = next(iter(identifiers.items()))

        item = db_session.get(model_class, identifier_value)
        if not item or getattr(item, 'deleted_at', None):
            raise ResourceNotFound(
                message=f"{model_class.__table__.info['name']} with {identifier_field} {identifier_value} not found",
            )

        if hasattr(data, 'model_dump'):
            payload = data.model_dump(exclude_unset=True)
        elif hasattr(data, 'dict'):
            payload = data.dict(exclude_unset=True)
        else:
            payload = dict(data)

        updateable_fields = getattr(model_class, 'updateable_fields', [])
        invalid_fields = [field for field in payload if field not in updateable_fields]
        if invalid_fields:
            raise InvalidRequestData(
                errors=[
                    {
                        'field': field,
                        'description': 'Field cannot be updated',
                    }
                    for field in invalid_fields
                ],
                message='Invalid fields in update request',
            )

        # Use the model's helper to apply the updates; it already validates fields
        item.update(payload)
        db_session.flush()
        db_session.refresh(item)

        relationships = get_model_relationships(model_class, db_session)
        return model_class.get_items(
            db_session=db_session,
            id=item.id,
            details=True,
            joins=relationships['joins'],
            list_joins=relationships['list_joins'],
        )

    @staticmethod
    def delete(model_class, db_session, **identifiers):
        if not identifiers:
            raise InvalidRequestData(
                message='Missing identifier for delete request',
            )

        identifier_field, identifier_value = next(iter(identifiers.items()))

        item = db_session.get(model_class, identifier_value)
        if not item:
            raise ResourceNotFound(
                message=f"{model_class.__table__.info['name']} with {identifier_field} {identifier_value} not found",
            )

        deleted_at_column = getattr(model_class, 'deleted_at', None)
        if deleted_at_column is not None:
            setattr(item, 'deleted_at', datetime.now(UTC))
            db_session.flush()
            db_session.refresh(item)
            return {
                'id': item.id,
                'deleted': True,
                'deleted_at': item.deleted_at.isoformat() if item.deleted_at else None,
            }

        db_session.delete(item)
        db_session.flush()
        return {
            'id': identifier_value,
            'deleted': True,
        }


class UserActions:
    @staticmethod
    def get_one_user(id_user, db_session):
        user = User.get_items(
            db_session=db_session,
            id=id_user,
            details=True,
            joins=[
                {
                    'model': Role,
                    'column': 'id_role',
                    'as_': 'role_details',
                },
            ],
            list_joins=[],
        )

        if not user:
            raise ResourceNotFound(
                message=f'User with ID {id_user} not found',
            )

        return user

    @staticmethod
    def get_all_users(
        db_session: Session,
        filters,
        sort_details,
        q,
        secondary_models_map,
        pagination={},
    ):
        users, pagination = User.get_items(
            db_session=db_session,
            sort_details=sort_details,
            filters=filters,
            details=True,
            q=q,
            pagination=pagination,
            secondary_models_map=secondary_models_map,
            joins=[
                {
                    'model': Role,
                    'column': 'id_role',
                    'as_': 'role_details',
                },
            ],
            list_joins=[],
        )

        return users, pagination

    @staticmethod
    def create_user(data, db_session: Session):
        # Check if user already exists
        if db_session.query(User).filter_by(email=data['email']).first():
            raise InvalidRequestData(
                errors=[{
                    'field': 'email',
                    'description': 'User with email already exists',
                }],
                message='User already exists',
            )

        # Check if role exists
        if 'id_role' in data and data['id_role'] is not None:
            if not db_session.get(Role, data['id_role']):
                raise InvalidRequestData(
                    errors=[{
                        'field': 'id_role',
                        'description': 'Role not found',
                    }],
                    message=f"Role with ID {data['id_role']} not found",
                )

        # Hash password using bcrypt directly
        password_hash = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt(),
        ).decode('utf-8')

        user = User(
            name=data['name'],
            email=data['email'],
            password=password_hash,
            id_role=data.get('id_role'),
            status='active',
        )
        db_session.add(user)
        db_session.flush()

        return user.to_dict()

    @staticmethod
    def update_user(id_user, data, db_session: Session, current_user: User):
        user = db_session.get(User, id_user)
        if not user:
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'User not found',
                    'type': 'user_not_found'
                }],
                message='User not found',
                http_status=404,
            )

        # Also cannot update the current user
        if user.email == current_user.email:
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'Cannot update the current user',
                    'type': 'invalid_operation'
                }],
            )

        # Check if user is trying to update their password
        if 'password' in data:
            password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            data['password'] = password_hash

        # Check if user is trying to update their role
        if 'id_role' in data and data['id_role'] is not None:
            role = db_session.get(Role, data['id_role'])
            if not role:
                raise InvalidRequestData(
                    errors=[{
                        'field': 'id_role',
                        'description': 'Role not found',
                        'type': 'role_not_found'
                    }],
                    message=f"Role with ID {data['id_role']} not found",
                )

        # Check if email is being updated but is used by someone else
        if 'email' in data:
            other_user = db_session.query(User).filter_by(email=data['email']).first()
            if other_user and other_user.id != id_user:
                raise InvalidRequestData(
                    errors=[{
                        'field': 'email',
                        'description': 'Email already in use',
                        'type': 'duplicate_email'
                    }],
                    message=f"Email {data['email']} is already in use",
                )
        user.update(data)

        return user.to_dict()

    @staticmethod
    def deactivate_user(id_user, db_session: Session, current_user: User):
        user = db_session.get(User, id_user)
        if not user:
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'User not found',
                    'type': 'user_not_found'
                }],
                message='User not found',
                http_status=404,
            )

        # Also cannot deactivate the current user
        if user.email == current_user.email:
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'Cannot deactivate the current user',
                    'type': 'invalid_operation'
                }],
                message='Cannot deactivate the current user',
            )

        # Check if user is already deactivated
        if user.status == 'deactivated':
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'User is already deactivated',
                    'type': 'already_deactivated'
                }],
                message='User is already deactivated',
            )

        # Deactivate user
        user.status = 'deactivated'
        user.last_deactivated_at = datetime.now(UTC)

        return user.to_dict()

    @staticmethod
    def activate_user(id_user, db_session: Session, current_user: User):
        user = db_session.get(User, id_user)
        if not user:
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'User not found',
                    'type': 'user_not_found'
                }],
                message='User not found',
                http_status=404,
            )

        # Check if user is already active
        if user.status == 'active':
            raise InvalidRequestData(
                errors=[{
                    'field': 'id_user',
                    'description': 'User is already activated',
                    'type': 'already_activated'
                }],
                message='User is already activated',
            )

        # Activate user
        user.status = 'active'
        user.last_activated_at = datetime.now(UTC)

        return user.to_dict()


class AuthActions:
    @staticmethod
    def _generate_unique_anonymous_token(db_session: Session) -> str:
        """
        Generate a unique anonymous token not present in DB.
        """

        for _ in range(10):
            token = uuid.uuid4().hex
            exists = db_session.query(User).filter_by(anonymous_token=token).first()
            if not exists:
                return token

        raise InternalServerError(message='Could not generate unique anonymous token')

    @staticmethod
    def _hash_password(raw_password: str) -> str:
        """
        Hash password using bcrypt.
        """

        return bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _encode_jwt(payload: dict) -> str:
        """
        Encode a JWT using HS256 with SECRET_KEY.
        """

        secret = os.getenv('SECRET_KEY')
        # Optional: add iat/exp to tokens; keep generous expiry for anonymous
        now = datetime.now(UTC)
        body = {
            **payload,
            'iat': int(now.timestamp()),
            # 90 days
            'exp': int((now + timedelta(days=90)).timestamp()),
        }
        return jwt.encode(body, secret, algorithm='HS256')

    @staticmethod
    def _decode_jwt(token: str) -> dict | None:
        """
        Use shared helper to decode and validate JWT.
        """

        return decode_jwt_token(token)

    @staticmethod
    def register_anonymous_user(jwt_token: str | None, db_session: Session) -> dict:
        """
        Create an anonymous user and return a JWT.

        If a valid JWT is present in the Authorization header, raise 422.
        """

        # If a JWT exists and is valid, return 422
        if jwt_token:
            claims = AuthActions._decode_jwt(jwt_token)
            if claims:
                raise InvalidRequestData(
                    message='Anonymous user is already authenticated',
                    http_status=422,
                )

            existing = db_session.get(User, 1)
            if existing:
                # Issue JWT for existing anonymous user
                jwt_token = AuthActions._encode_jwt({
                    'sub': str(existing.id),
                    'anonymous_token': jwt_token,
                })
                return {
                    'jwt': jwt_token,
                    'user': existing.to_dict(),
                }

            # Create a fresh anonymous user using provided token
            anon_token = jwt_token
        else:
            # No bearer provided: generate a fresh token
            anon_token = AuthActions._generate_unique_anonymous_token(db_session)

        # For now, the only role is the default "Dummy" role
        default_role_id = 1

        # Email format for anonymous users is <token>@anonymous.local
        email = f'{anon_token}@anonymous.local'
        # Password is the same as the token. But no login option for anonymous
        # users available so it's safe.
        password_hash = AuthActions._hash_password(anon_token)

        user = User(
            name='Anonymous',
            email=email,
            password=password_hash,
            id_role=default_role_id,
            status='active',
            is_anonymous=True,
            is_customer=False,
            anonymous_token=anon_token,
        )
        db_session.add(user)
        db_session.flush()

        # Build JWT with required claims
        jwt_token = AuthActions._encode_jwt({
            'sub': str(user.id),
            'anonymous_token': anon_token,
        })

        return {
            'jwt': jwt_token,
            'user': user.to_dict(),
        }

class OrganizationActions:
    pass


class MetadataActions:
    @staticmethod
    def get_all_metadata_objects(db_session: Session, pagination={}):
        metadata_objects, pagination = MetadataObject.get_items(
            db_session=db_session,
            details=True,
            pagination=pagination,
            q='',
            secondary_models_map={},
            joins=[],
            list_joins=[
                {
                    'model': MetadataField,
                    'column': 'id_metadata_object',
                    'as_': 'metadata_fields_details',
                    'sort_by': 'id',
                    'reverse': True,
                    'limit': 500,
                },
            ],
        )
        return metadata_objects, pagination


class FileActions:
    @staticmethod
    def upload_file(request: FastAPIRequest, file: UploadFile, db_session: Session):
        if not file.filename:
            raise InvalidRequestData(message='File name is required')

        content_length = None
        if hasattr(request, 'content_length') and request.content_length:
            content_length = request.content_length
        if not content_length and hasattr(request, 'headers') and request.headers:
            cl_header = request.headers.get('content-length') or request.headers.get('Content-Length')
            if cl_header:
                try:
                    content_length = int(cl_header)
                except Exception:
                    content_length = None
        if not content_length:
            try:
                file_obj = getattr(file, 'file', None) or file
                pos = file_obj.tell()
                file_obj.seek(0, os.SEEK_END)
                content_length = file_obj.tell()
                file_obj.seek(pos, os.SEEK_SET)
            except Exception:
                content_length = None
        if not content_length:
            raise InvalidRequestData(message='Could not determine file size')
        if content_length > 30 * 1024 * 1024:
            raise InvalidRequestData(message='File must be less than 30MB')
        if content_length < 1024:
            raise InvalidRequestData(message='File must be greater than 1KB')

        uploads_dir = 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        original_ext = os.path.splitext(file.filename)[1]
        stored_name = f"upload_{uuid.uuid4()}{original_ext}"
        dest_path = os.path.join(uploads_dir, stored_name)

        file_stream = getattr(file, 'file', None) or getattr(file, 'stream', None)
        if not file_stream:
            raise InvalidRequestData(message='Could not access file stream')
        try:
            file_stream.seek(0, os.SEEK_SET)
        except Exception:
            pass

        with open(dest_path, 'wb') as out_file:
            while True:
                chunk = file_stream.read(1024 * 1024)
                if not chunk:
                    break
                out_file.write(chunk)

        return {
            'file_name': file.filename,
            'stored_name': stored_name,
            'file_path': dest_path,
            'content_type': getattr(file, 'content_type', None),
            'size': content_length,
            'status': 'stored',
        }

    # This is called by the Celery worker
    @staticmethod
    def process_transduction_task(task_id: int):
        """Run OCR/translation for a task in the background and persist results."""

        print(f'Processing transduction task {task_id}...')
        
        # Send initial progress update
        from backend.helpers import send_websocket_task_update
        send_websocket_task_update(
            task_id=task_id,
            status="started",
            message="Task processing started",
            data={"task_id": task_id}
        )
        
        db_session = SessionLocal()
        try:
            task: TransductionTask|None = db_session.get(TransductionTask, task_id)
            if not task:
                error_msg = f'task_not_found:{task_id}'
                send_websocket_task_update(
                    task_id=task_id,
                    status="failed",
                    message=f"Task {task_id} not found",
                    data={"error": error_msg}
                )
                return {
                    'status': 'failed',
                    'reason': error_msg,
                }

            print(f'Task found: {task}')

            # Respect pre-start cancellation
            if ((task.params or {}).get('cancel_requested')) or task.status == TransductionTaskStatusEnum.CANCELLED.value:
                task.status = TransductionTaskStatusEnum.CANCELLED.value
                task.completed_at = datetime.now(UTC)

                db_session.commit()

                send_websocket_task_update(
                    task_id=task_id,
                    status='cancelled',
                    message='Task was cancelled before start',
                    data={'task_id': task_id}
                )
                return {'status': 'cancelled', 'task_id': task_id}

            task.status = TransductionTaskStatusEnum.PROCESSING.value
            task.started_at = datetime.now(UTC)

            params = task.params or {}
            file_ids = params.get('file_ids') or []
            translate = bool(params.get('translate'))
            transliterate = bool(params.get('transliterate'))
            ocr_model = params.get('ocr_model')

            send_websocket_task_update(
                task_id=task_id,
                status="processing",
                message="Task is now being processed",
                data={"task_id": task_id, "status": "processing", "file_count": len(file_ids)}
            )

            all_ok = True
            results = []

            print(f'Processing {len(file_ids)} files...')

            def cancel_requested_now() -> bool:
                try:
                    latest = db_session.get(TransductionTask, task_id)
                    return bool((latest.params or {}).get('cancel_requested') or latest.status == TransductionTaskStatusEnum.CANCELLED.value)
                except Exception:
                    return False

            def register_runpod_job(job_id: str, file_id_for_job: int):
                try:
                    latest = db_session.get(TransductionTask, task_id)
                    params_latest = (latest.params or {}).copy()
                    jobs = list(params_latest.get('runpod_jobs') or [])
                    jobs.append({'job_id': job_id, 'file_id': file_id_for_job})
                    params_latest['runpod_jobs'] = jobs
                    latest.params = params_latest
                    db_session.commit()
                except Exception:
                    # Best-effort tracking; not critical
                    pass

            for file_id in file_ids:
                # Check cancellation between files
                if cancel_requested_now():
                    task.status = TransductionTaskStatusEnum.CANCELLED.value
                    task.completed_at = datetime.now(UTC)
                    db_session.commit()
                    send_websocket_task_update(
                        task_id=task_id,
                        status='cancelled',
                        message='Task cancelled during processing',
                        data={'file_id': file_id}
                    )
                    return {'status': 'cancelled', 'task_id': task_id}

                record = db_session.get(TransductionTaskFile, file_id)
                if not record:
                    all_ok = False
                    results.append({
                        'file_id': file_id,
                        'status': 'failed',
                        'reason': 'file_not_found',
                    })
                    continue

                if not record.id_transduction_task:
                    record.id_transduction_task = task.id

                provider_key = 'mistral' if ocr_model != 'qari' else 'qari'

                send_websocket_task_update(
                    task_id=task_id,
                    status="processing_file",
                    message=f"Processing file: {record.file_name}",
                    data={
                        "file_id": file_id,
                        "file_name": record.file_name,
                        "file_type": record.file_type,
                        "provider": provider_key
                    }
                )

                if provider_key == 'qari':
                    print(f'Extracting text with Qari for {record.file_path}...')
                    send_websocket_task_update(
                        task_id=task_id,
                        status="ocr_started",
                        message=f"Starting OCR with Qari for {record.file_name}",
                        data={"file_id": file_id, "provider": "qari"}
                    )
                    
                    ocr_result = TransductionTaskFileActions.extract_text_with_qari(
                        dest_path=record.file_path,
                        file_type=record.file_type,
                        cancel_checker=cancel_requested_now,
                        register_job_fn=lambda job_id, fid=file_id: register_runpod_job(job_id, fid),
                    )
                    
                    # Send OCR completion update
                    if ocr_result.get('status') == 'completed':
                        send_websocket_task_update(
                            task_id=task_id,
                            status="ocr_completed",
                            message=f"OCR completed for {record.file_name}",
                            data={
                                "file_id": file_id,
                                "provider": "qari",
                                "text_length": len(ocr_result.get('ocr_text', ''))
                            }
                        )
                    else:
                        send_websocket_task_update(
                            task_id=task_id,
                            status="ocr_failed",
                            message=f"OCR failed for {record.file_name}: {ocr_result.get('reason')}",
                            data={
                                "file_id": file_id,
                                "provider": "qari",
                                "error": ocr_result.get('reason')
                            }
                        )
                else:
                    print(f'Extracting text with Mistral for {record.file_path}...')
                    send_websocket_task_update(
                        task_id=task_id,
                        status="ocr_started",
                        message=f"Starting OCR with Mistral for {record.file_name}",
                        data={"file_id": file_id, "provider": "mistral"}
                    )
                    
                    ocr_result = TransductionTaskFileActions.extract_text_with_mistral(
                        dest_path=record.file_path,
                        file_type=record.file_type,
                        cancel_checker=cancel_requested_now,
                    )
                    
                    # Send OCR completion update
                    if ocr_result.get('status') == 'completed':
                        send_websocket_task_update(
                            task_id=task_id,
                            status="ocr_completed",
                            message=f"OCR completed for {record.file_name}",
                            data={
                                "file_id": file_id,
                                "provider": "mistral",
                                "text_length": len(ocr_result.get('ocr_text', ''))
                            }
                        )
                    else:
                        send_websocket_task_update(
                            task_id=task_id,
                            status="ocr_failed",
                            message=f"OCR failed for {record.file_name}: {ocr_result.get('reason')}",
                            data={
                                "file_id": file_id,
                                "provider": "mistral",
                                "error": ocr_result.get('reason')
                            }
                        )

                openai_result = None
                transliteration_result = None
                docx_path = None
                translation_text = None
                transliteration_text = None

                # Check cancellation before translation
                if cancel_requested_now():
                    task.status = TransductionTaskStatusEnum.CANCELLED.value
                    task.completed_at = datetime.now(UTC)
                    db_session.commit()
                    send_websocket_task_update(
                        task_id=task_id,
                        status='cancelled',
                        message='Task cancelled before translation',
                        data={'file_id': file_id}
                    )
                    return {'status': 'cancelled', 'task_id': task_id}

                if translate:
                    print(f'Translating text with OpenAI for {record.file_path}...')
                    send_websocket_task_update(
                        task_id=task_id,
                        status='translation_started',
                        message=f'Starting translation for {record.file_name}',
                        data={'file_id': file_id}
                    )
                    
                    openai_result = TransductionTaskFileActions.translate_text_with_openai(
                        arabic_text=(ocr_result.get('ocr_text') or ''),
                    )
                    if openai_result and openai_result.get('status') == 'completed' and openai_result.get('translation'):
                        translation_text = openai_result.get('translation')

                # Check cancellation before transliteration
                if cancel_requested_now():
                    task.status = TransductionTaskStatusEnum.CANCELLED.value
                    task.completed_at = datetime.now(UTC)
                    db_session.commit()
                    send_websocket_task_update(
                        task_id=task_id,
                        status='cancelled',
                        message='Task cancelled before transliteration',
                        data={'file_id': file_id}
                    )
                    return {'status': 'cancelled', 'task_id': task_id}

                if transliterate:
                    print(f'Transliterating text with OpenAI for {record.file_path}...')
                    send_websocket_task_update(
                        task_id=task_id,
                        status='transliteration_started',
                        message=f'Starting transliteration for {record.file_name}',
                        data={'file_id': file_id}
                    )
                    
                    transliteration_result = TransductionTaskFileActions.transliterate_text_with_openai(
                        arabic_text=(ocr_result.get('ocr_text') or '')
                    )

                    if transliteration_result and transliteration_result.get('status') == 'completed' and transliteration_result.get('transliteration'):
                        transliteration_text = transliteration_result.get('transliteration')
                        send_websocket_task_update(
                            task_id=task_id,
                            status='transliteration_completed',
                            message=f'Transliteration completed for {record.file_name}',
                            data={'file_id': file_id}
                        )
                    else:
                        send_websocket_task_update(
                            task_id=task_id,
                            status='transliteration_failed',
                            message=f"Transliteration failed for {record.file_name}: {transliteration_result.get('reason') if transliteration_result else 'unknown'}",
                            data={'file_id': file_id, 'error': (transliteration_result or {}).get('reason')}
                        )

                # Generate DOCX if we have either translation or transliteration
                # Check cancellation before docx generation
                if cancel_requested_now():
                    task.status = TransductionTaskStatusEnum.CANCELLED.value
                    task.completed_at = datetime.now(UTC)
                    db_session.commit()
                    send_websocket_task_update(
                        task_id=task_id,
                        status='cancelled',
                        message='Task cancelled before DOCX generation',
                        data={'file_id': file_id}
                    )
                    return {'status': 'cancelled', 'task_id': task_id}

                if (translation_text or transliteration_text):
                    print(f'Generating docx file for {record.file_path}...')
                    send_websocket_task_update(
                        task_id=task_id,
                        status='docx_generation_started',
                        message=f'Generating DOCX file for {record.file_name}',
                        data={'file_id': file_id}
                    )
                    
                    docx_path = TransductionTaskFileActions.generate_docx_file(
                        translation_text=translation_text,
                        transliteration_text=transliteration_text,
                        original_text=ocr_result.get('ocr_text'),
                    )
                    
                    send_websocket_task_update(
                        task_id=task_id,
                        status='docx_generated',
                        message=f'DOCX file generated for {record.file_name}',
                        data={'file_id': file_id, 'docx_path': docx_path}
                    )

                file_ok = (ocr_result.get('status') == 'completed') and (not translate or (openai_result and openai_result.get('status') == 'completed'))
                all_ok = all_ok and file_ok

                # Optionally persist per-file meta
                try:
                    record.meta = (record.meta or {}) | {
                        'provider': provider_key,
                        'ocr': ocr_result,
                        'translation': openai_result if openai_result else ({'status': 'skipped'} if not translate else {'status': 'failed'}),
                        'transliteration': transliteration_result if transliteration_result else ({'status': 'skipped'} if not transliterate else {'status': 'failed'}),
                        'docx_path': docx_path,
                    }
                except Exception:
                    # meta update is best-effort
                    pass

                results.append({
                    'file_id': record.id,
                    'file_name': record.file_name,
                    'file_path': record.file_path,
                    'file_type': record.file_type,
                    'provider': provider_key,
                    'ocr': ocr_result,
                    'translation': openai_result if openai_result else ({'status': 'skipped'} if not translate else {'status': 'failed'}),
                    'transliteration': transliteration_result if transliteration_result else ({'status': 'skipped'} if not transliterate else {'status': 'failed'}),
                    'docx_path': docx_path,
                })

                # Send file completion update
                send_websocket_task_update(
                    task_id=task_id,
                    status="file_completed",
                    message=f"File {record.file_name} processing completed",
                    data={
                        "file_id": file_id,
                        "file_name": record.file_name,
                        "ocr_status": ocr_result.get('status'),
                        "translation_status": openai_result.get('status') if translate else None
                    }
                )

            task.result = {
                'files': results,
            }
            task.status = (
                TransductionTaskStatusEnum.SUCCEEDED.value
                if all_ok
                else TransductionTaskStatusEnum.FAILED.value
            )
            task.completed_at = datetime.now(UTC)

            if all_ok:
                send_websocket_task_update(
                    task_id=task_id,
                    status="completed",
                    message="Task processing completed successfully",
                    data={"task_id": task_id, "files_processed": len(results)}
                )
            else:
                send_websocket_task_update(
                    task_id=task_id,
                    status="failed",
                    message="Task processing failed",
                    data={"task_id": task_id, "files_processed": len(results)}
                )

            db_session.commit()

            return {
                'status': task.status,
                'task_id': task.id,
                'results': results,
            }

        except Exception as e:
            try:
                if 'task' in locals() and task is not None:
                    task.status = TransductionTaskStatusEnum.FAILED.value
                    task.completed_at = datetime.now(UTC)
                    db_session.commit()
            except Exception:
                pass
            
            error_msg = f'error:{e.__class__.__name__}: {e}'
            send_websocket_task_update(
                task_id=task_id,
                status="error",
                message=f"Error processing task: {e}",
                data={"task_id": task_id, "error": str(e)}
            )
            
            return {
                'status': 'failed',
                'reason': error_msg,
            }
        finally:
            db_session.close()

    @staticmethod
    def get_all_transduction_tasks(claims: dict, db_session: Session, pagination={}):
        try:
            user_id = int((claims or {}).get('sub'))
        except Exception:
            user_id = None

        if not user_id:
            raise Unauthorized(message='Missing or invalid user claims', http_status=401)

        tasks, pagination = TransductionTask.get_items(
            db_session=db_session,
            details=True,
            pagination=pagination,
            filters=[
                {
                    'model': TransductionTask,
                    'field': 'id_user_created_by',
                    'equal_to': user_id,
                }
            ],
        )
        return tasks, pagination

    @staticmethod
    def get_one_transduction_task(id_transduction_task: int, claims: dict, db_session: Session):
        try:
            user_id = int((claims or {}).get('sub'))
        except Exception:
            raise Unauthorized(message='Missing or invalid user claims', http_status=401)

        task = TransductionTask.get_items(
            db_session=db_session,
            id=id_transduction_task,
            details=True,
        )
        if not task:
            raise ResourceNotFound(
                message=f'Transduction Task with ID {id_transduction_task} not found',
            )

        if task.get('id_user_created_by') != user_id:
            raise Forbidden(message='You do not have access to this transduction task')

        return task

    @staticmethod
    def cancel_transduction_task(id_transduction_task: int, request: dict, claims: dict, db_session: Session):
        # Validate requester identity
        try:
            user_id = int((claims or {}).get('sub'))
        except Exception:
            raise Unauthorized(message='Missing or invalid user claims', http_status=401)

        task: TransductionTask|None = db_session.get(TransductionTask, id_transduction_task)
        if not task:
            raise ResourceNotFound(
                message=f'Transduction Task with ID {id_transduction_task} not found',
            )

        # Enforce ownership: only creator can cancel
        if task.id_user_created_by != user_id:
            raise Forbidden(message='You do not have permission to cancel this task')

        # If already cancelled, reject the operation
        if task.status == TransductionTaskStatusEnum.CANCELLED.value:
            raise InvalidRequestData(
                errors=[{
                    'field': 'status',
                    'description': 'Task is already cancelled',
                }],
                message='Task already cancelled',
                http_status=422,
            )

        # Flag cancellation in params
        try:
            params = task.params or {}
            params['cancel_requested'] = True
            task.params = params
        except Exception:
            pass

        # Revoke Celery task if known
        try:
            from backend.celery_app import celery as celery_app
            celery_task_id = (task.params or {}).get('celery_task_id')
            if celery_task_id:
                celery_app.control.revoke(celery_task_id, terminate=True, signal='SIGKILL')
        except Exception:
            pass

        # Cancel any pending RunPod jobs recorded in params
        try:
            params = task.params or {}
            jobs = params.get('runpod_jobs') or []
            runpod_token = os.getenv('RUNPOD_TOKEN')
            runpod_endpoint_id = os.getenv('RUNPOD_ENDPOINT_ID', 'rm7e86qv9j9o0p')
            if runpod_token and jobs:
                headers = {
                    'Authorization': f'Bearer {runpod_token}',
                    'Content-Type': 'application/json',
                }
                for job in jobs:
                    job_id = job.get('job_id')
                    if not job_id:
                        continue
                    try:
                        cancel_url = f'https://api.runpod.ai/v2/{runpod_endpoint_id}/cancel/{job_id}'
                        requests.post(cancel_url, headers=headers, timeout=15)
                    except Exception:
                        # Continue cancelling others even if one fails
                        continue
        except Exception:
            pass

        # If task is still active, mark cancelled now; otherwise leave terminal status as-is
        if task.status in (
            TransductionTaskStatusEnum.CREATED.value,
            TransductionTaskStatusEnum.QUEUED.value,
            TransductionTaskStatusEnum.PROCESSING.value,
        ):
            task.status = TransductionTaskStatusEnum.CANCELLED.value
            task.completed_at = datetime.now(UTC)

        # Best-effort websocket notify
        try:
            from backend.helpers import send_websocket_task_update
            send_websocket_task_update(
                task_id=task.id,
                status='cancelled',
                message='Cancellation requested',
                data={'task_id': task.id},
            )
        except Exception:
            pass

        return task.to_dict()


class TransductionTaskFileActions:
    @staticmethod
    def extract_text_with_mistral(dest_path: str, file_type: str, cancel_checker=None):
        """
        Perform OCR on Arabic content in an image or PDF using Mistral.

        Returns a dict: {
            'status': 'skipped'|'attempted'|'completed'|'failed',
            'reason': str|None,
            'model': str|None,
            'ocr_text': str|None,
        }
        """

        mistral_result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'ocr_text': None,
        }

        api_key = os.getenv('MISTRAL_API_KEY')
        mistral_model = os.getenv('MISTRAL_OCR_MODEL', os.getenv('MISTRAL_TRANSLATION_MODEL', 'pixtral-large-latest'))
        if not api_key:
            mistral_result['reason'] = 'MISTRAL_API_KEY not set'
            return mistral_result

        # If file type is pdf, convert each page to png using pdf2image and process concurrently
        pdf_to_png_paths = []
        if file_type == 'pdf':
            try:
                pdf_pages = pdf2image.convert_from_path(dest_path)
                for page_num, page in enumerate(pdf_pages[:max_pages]):
                    page_path = f'{dest_path}_page_{page_num}.png'
                    page.save(page_path, 'PNG')
                    pdf_to_png_paths.append(page_path)
                if pdf_to_png_paths:
                    return TransductionTaskFileActions._process_multiple_images_with_mistral(
                        pdf_to_png_paths,
                        cancel_checker=cancel_checker,
                    )
            except Exception as e:
                mistral_result['status'] = 'failed'
                mistral_result['reason'] = f'Failed to convert PDF to images: {e}'
                return mistral_result

        try:
            mistral_prompt = 'Extract the Arabic text from the provided content verbatim. Do not translate. Return only the extracted Arabic text. Do not add any other text or comments.'

            with MistralClient(api_key=api_key) as mistral_client:
                mistral_result['status'] = 'attempted'
                mistral_result['model'] = mistral_model

                if file_type in ('jpg', 'png', 'jpeg'):
                    mime_type = 'image/jpeg' if file_type in ('jpg', 'jpeg') else 'image/png'
                    with open(dest_path, 'rb') as f:
                        image_b64 = base64.b64encode(f.read()).decode('ascii')

                    ocr_text = None

                    responses_api = getattr(mistral_client, 'responses', None)
                    if responses_api is not None:
                        try:
                            response = responses_api.create(  # type: ignore[attr-defined]
                                model=mistral_model,
                                input=[{
                                    'role': 'user',
                                    'content': [
                                        {'type': 'text', 'text': mistral_prompt},
                                        {'type': 'input_image', 'mime_type': mime_type, 'image': image_b64},
                                    ],
                                }],
                            )
                            if hasattr(response, 'output_text'):
                                ocr_text = response.output_text  # type: ignore[attr-defined]
                            else:
                                ocr_text = str(response)
                        except Exception:
                            # Fall back to chat with data URL if responses call fails
                            pass

                    if ocr_text is None:
                        try:
                            data_url = f"data:{mime_type};base64,{image_b64}"
                            messages = [{
                                'role': 'user',
                                'content': [
                                    {'type': 'text', 'text': mistral_prompt},
                                    {'type': 'image_url', 'image_url': {'url': data_url}},
                                ],
                            }]
                            chat_resp = mistral_client.chat.complete(
                                model=mistral_model,
                                messages=messages,
                            )
                            if getattr(chat_resp, 'choices', None):
                                choice0 = chat_resp.choices[0]
                                if getattr(choice0, 'message', None) and getattr(choice0.message, 'content', None):
                                    ocr_text = choice0.message.content
                            if ocr_text is None:
                                ocr_text = str(chat_resp)
                        except Exception:
                            # Fall back to chat with data URL if responses call fails
                            pass

                    if ocr_text:
                        mistral_result['status'] = 'completed'
                        mistral_result['ocr_text'] = ocr_text

                elif file_type == 'pdf':
                    # This branch is now handled earlier by converting to images and processing concurrently
                    mistral_result['reason'] = 'Internal: PDF should have been handled via image conversion'
                else:
                    mistral_result['reason'] = f'Unsupported file_type: {file_type}'

        except Exception as e:
            mistral_result['status'] = 'failed'
            mistral_result['reason'] = f'Setup error: {e.__class__.__name__}: {e}'

        return mistral_result

    @staticmethod
    def _process_single_image_with_mistral(dest_path: str, file_type: str):
        """Process a single image with Mistral OCR."""
        mistral_result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'ocr_text': None,
        }

        api_key = os.getenv('MISTRAL_API_KEY')
        mistral_model = os.getenv('MISTRAL_OCR_MODEL', os.getenv('MISTRAL_TRANSLATION_MODEL', 'pixtral-large-latest'))
        if not api_key:
            mistral_result['reason'] = 'MISTRAL_API_KEY not set'
            return mistral_result

        try:
            mistral_prompt = 'Extract the Arabic text from the provided content verbatim. Do not translate. Return only the extracted Arabic text. Do not add any other text or comments.'

            with MistralClient(api_key=api_key) as mistral_client:
                mistral_result['status'] = 'attempted'
                mistral_result['model'] = mistral_model

                if file_type in ('jpg', 'png', 'jpeg'):
                    mime_type = 'image/jpeg' if file_type in ('jpg', 'jpeg') else 'image/png'
                    with open(dest_path, 'rb') as f:
                        image_b64 = base64.b64encode(f.read()).decode('ascii')

                    ocr_text = None

                    responses_api = getattr(mistral_client, 'responses', None)
                    if responses_api is not None:
                        try:
                            response = responses_api.create(  # type: ignore[attr-defined]
                                model=mistral_model,
                                input=[{
                                    'role': 'user',
                                    'content': [
                                        {'type': 'text', 'text': mistral_prompt},
                                        {'type': 'input_image', 'mime_type': mime_type, 'image': image_b64},
                                    ],
                                }],
                            )
                            if hasattr(response, 'output_text'):
                                ocr_text = response.output_text  # type: ignore[attr-defined]
                            else:
                                ocr_text = str(response)
                        except Exception:
                            pass

                    if ocr_text is None:
                        try:
                            data_url = f"data:{mime_type};base64,{image_b64}"
                            messages = [{
                                'role': 'user',
                                'content': [
                                    {'type': 'text', 'text': mistral_prompt},
                                    {'type': 'image_url', 'image_url': {'url': data_url}},
                                ],
                            }]
                            chat_resp = mistral_client.chat.complete(
                                model=mistral_model,
                                messages=messages,
                            )
                            if getattr(chat_resp, 'choices', None):
                                choice0 = chat_resp.choices[0]
                                if getattr(choice0, 'message', None) and getattr(choice0.message, 'content', None):
                                    ocr_text = choice0.message.content
                            if ocr_text is None:
                                ocr_text = str(chat_resp)
                        except Exception:
                            pass

                    if ocr_text:
                        mistral_result['status'] = 'completed'
                        mistral_result['ocr_text'] = ocr_text
                else:
                    mistral_result['reason'] = f'Unsupported file_type: {file_type}'

        except Exception as e:
            mistral_result['status'] = 'failed'
            mistral_result['reason'] = f'Setup error: {e.__class__.__name__}: {e}'

        return mistral_result

    @staticmethod
    def _process_multiple_images_with_mistral(image_paths: list, cancel_checker=None):
        """Process multiple images with Mistral OCR concurrently and stitch results."""
        result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'ocr_text': None,
        }

        try:
            result['status'] = 'attempted'

            async def process_one(idx: int, image_path: str):
                single = await asyncio.to_thread(TransductionTaskFileActions._process_single_image_with_mistral, image_path, 'png')
                if single.get('status') == 'completed':
                    return {'page': idx, 'text': single.get('ocr_text'), 'model': single.get('model')}
                return {'page': idx, 'error': single.get('reason')}

            async def run_all():
                tasks = [process_one(i, p) for i, p in enumerate(image_paths)]
                return await asyncio.gather(*tasks, return_exceptions=False)

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Allow cooperative cancellation before starting heavy work
            try:
                if callable(cancel_checker) and cancel_checker():
                    result['status'] = 'failed'
                    result['reason'] = 'cancelled'
                    return result
            except Exception:
                pass

            results = loop.run_until_complete(run_all())

            # Cleanup temporary images
            for p in image_paths:
                try:
                    os.remove(p)
                except Exception:
                    pass

            successful = [r for r in results if 'text' in r and r['text']]
            if not successful:
                result['status'] = 'failed'
                result['reason'] = 'All pages failed'
                return result

            successful.sort(key=lambda r: r['page'])
            stitched = []
            for r in successful:
                stitched.append(f"[Page {r['page'] + 1}]\n{r['text']}")

            result['status'] = 'completed'
            result['ocr_text'] = '\n\n'.join(stitched)
            result['model'] = successful[0].get('model')
            return result

        except Exception as e:
            result['status'] = 'failed'
            result['reason'] = f'Mistral PDF error: {e.__class__.__name__}: {e}'
            # Attempt cleanup
            for p in image_paths:
                try:
                    os.remove(p)
                except Exception:
                    pass
            return result

    @staticmethod
    def extract_text_with_qari(dest_path: str, file_type: str, cancel_checker=None, register_job_fn=None):
        """
        Perform OCR on Arabic content using RunPod Qari API.

        Returns a dict: {
            'status': 'skipped'|'attempted'|'completed'|'failed',
            'reason': str|None,
            'model': str|None,
            'ocr_text': str|None,
        }
        """

        print(f'Extracting text with Qari for {dest_path}...')
        qari_result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'ocr_text': None,
        }

        # Normalize cancel checker: use callable cancel_checker if provided
        cancel_checker_fn = cancel_checker if callable(cancel_checker) else (lambda: False)
        job_registrar = register_job_fn if callable(register_job_fn) else None

        # If file type is pdf, convert each page to png using pdf2image
        pdf_to_png_paths = []
        if file_type == 'pdf':
            try:
                pdf_pages = pdf2image.convert_from_path(dest_path)
                for page_num, page in enumerate(pdf_pages[:max_pages]):
                    page_path = f'{dest_path}_page_{page_num}.png'
                    page.save(page_path, 'PNG')
                    pdf_to_png_paths.append(page_path)
                print(f'Converted PDF to {len(pdf_to_png_paths)} images')
            except Exception as e:
                qari_result['status'] = 'failed'
                qari_result['reason'] = f'Failed to convert PDF to images: {e}'
                print(f'PDF conversion failed: {e}')
                return qari_result

        # Handle PDF processing with multiple images
        if file_type == 'pdf' and pdf_to_png_paths:
            return TransductionTaskFileActions._process_multiple_images_with_qari(
                pdf_to_png_paths,
                cancel_checker=cancel_checker_fn,
                register_job_fn=job_registrar,
            )
        
        # Handle single image processing
        if file_type not in ('jpg', 'png'):
            qari_result['reason'] = f'Unsupported file_type for Qari: {file_type}'
            print(f'Unsupported file_type for Qari: {file_type}')
            return qari_result

        return TransductionTaskFileActions._process_single_image_with_qari(
            dest_path,
            file_type,
            cancel_checker=cancel_checker_fn,
            register_job_fn=job_registrar,
        )

    @staticmethod
    def _process_single_image_with_qari(dest_path: str, file_type: str, cancel_checker=None, register_job_fn=None):
        """
        Process a single image with Qari OCR.
        """

        qari_result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'ocr_text': None,
        }

        try:
            cancel_checker_fn = cancel_checker if callable(cancel_checker) else (lambda: False)
            job_registrar = register_job_fn if callable(register_job_fn) else None
            # Get RunPod API configuration from environment
            runpod_token = os.getenv('RUNPOD_TOKEN')
            runpod_endpoint_id = os.getenv('RUNPOD_ENDPOINT_ID', 'rm7e86qv9j9o0p')
            max_new_tokens = int(os.getenv('RUNPOD_MAX_NEW_TOKENS', '3000'))
            
            if not runpod_token:
                qari_result['status'] = 'failed'
                print(f'RUNPOD_TOKEN environment variable not set')
                qari_result['reason'] = 'RUNPOD_TOKEN environment variable not set'
                return qari_result

            qari_result['status'] = 'attempted'
            print(f'RUNPOD_TOKEN environment variable set')

            qari_result['model'] = 'Qari-OCR-via-RunPod'
            print(f'Qari model set to {qari_result["model"]}')

            # Convert local image to base64
            with open(dest_path, 'rb') as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            print(f'Image converted to base64')

            # Create data URL for the image
            mime_type = 'image/jpeg' if file_type == 'jpg' else 'image/png'
            image_data_url = f"data:{mime_type};base64,{image_base64}"
            print(f'Image data URL created')

            # Step 1: Send request to start processing
            run_url = f"https://api.runpod.ai/v2/{runpod_endpoint_id}/run"
            headers = {
                "Authorization": f"Bearer {runpod_token}",
                "Content-Type": "application/json"
            }
            print(f'Headers created')

            payload = {
                "input": {
                    "image_b64": image_data_url,
                    "max_new_tokens": max_new_tokens
                }
            }
            print(f'Payload created')

            # Send initial request
            response = requests.post(run_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            print(f'Request sent')

            run_data = response.json()
            if 'id' not in run_data:
                qari_result['status'] = 'failed'
                qari_result['reason'] = f'RunPod run request failed: {run_data}'
                return qari_result
            print(f'RunPod run request successful')

            task_id = run_data['id']
            # Persist job id for later cancellation
            try:
                if job_registrar:
                    job_registrar(task_id)
            except Exception:
                pass
            
            # Step 2: Poll status endpoint every 4 seconds until completion
            status_url = f"https://api.runpod.ai/v2/{runpod_endpoint_id}/status/{task_id}"
            max_wait_time = 300  # 5 minutes timeout
            start_time = time.time()
            print(f'Status URL created')

            while time.time() - start_time < max_wait_time:
                # Allow cooperative cancellation
                try:
                    if cancel_checker_fn():
                        qari_result['status'] = 'failed'
                        qari_result['reason'] = 'cancelled'
                        print('Qari OCR cancelled by request')
                        return qari_result
                except Exception:
                    pass
                try:
                    status_response = requests.post(status_url, headers=headers, timeout=30)
                    status_response.raise_for_status()
                    status_data = status_response.json()
                    
                    print(f'Status data: {status_data}')

                    if status_data.get('status') == 'COMPLETED':
                        # Extract OCR text from successful response
                        output = status_data.get('output', {})
                        if output.get('ok') and output.get('results'):
                            # Combine all successful OCR results (cleaning HTML-like markup)
                            ocr_texts = []
                            for result in output['results']:
                                if result.get('success') and result.get('text'):
                                    cleaned = _clean_qari_ocr_html_preserve_breaks(result['text'])
                                    if cleaned:
                                        ocr_texts.append(cleaned)

                            if ocr_texts:
                                qari_result['status'] = 'completed'
                                qari_result['ocr_text'] = '\n\n'.join(ocr_texts)
                                qari_result['model'] = output.get('model', 'Qari-OCR-via-RunPod')
                                print(f'Qari OCR completed')
                                return qari_result
                            else:
                                qari_result['status'] = 'failed'
                                qari_result['reason'] = 'No successful OCR results found'
                                print(f'Qari OCR failed')
                                return qari_result
                        else:
                            qari_result['status'] = 'failed'
                            qari_result['reason'] = f'RunPod processing failed: {output}'
                            print(f'Qari OCR failed')
                            return qari_result
                    
                    elif status_data.get('status') == 'FAILED':
                        # Handle error response format
                        error_msg = status_data.get('error', 'Unknown error')
                        output = status_data.get('output', {})
                        if output.get('ok') == False:
                            qari_result['status'] = 'failed'
                            qari_result['reason'] = f'RunPod processing failed: {error_msg}'
                            print(f'Qari OCR failed')
                            return qari_result
                        else:
                            qari_result['status'] = 'failed'
                            qari_result['reason'] = f'RunPod task failed: {error_msg}'
                            print(f'Qari OCR failed')
                            return qari_result
                    
                    elif status_data.get('status') == 'IN_PROGRESS':
                        # Still processing, wait 4 seconds before next poll
                        time.sleep(4)
                        print(f'Qari OCR in progress')
                        continue
                    
                    else:
                        # Unknown status, wait and retry
                        time.sleep(4)
                        print(f'Qari OCR unknown status')
                        continue
                        
                except requests.exceptions.RequestException as e:
                    # Network error, wait and retry
                    time.sleep(4)
                    print(f'Qari OCR network error')
                    continue
            
            # Timeout reached
            qari_result['status'] = 'failed'
            qari_result['reason'] = f'RunPod task timed out after {max_wait_time} seconds'
            print(f'Qari OCR timed out')

        except Exception as e:
            qari_result['status'] = 'failed'
            qari_result['reason'] = f'Qari error: {e.__class__.__name__}: {e}'
            print(f'Qari OCR failed: {e.__class__.__name__}: {e}')

        return qari_result

    @staticmethod
    def _process_multiple_images_with_qari(image_paths: list, cancel_checker=None, register_job_fn=None):
        """Process multiple images with Qari OCR asynchronously and stitch results."""
        qari_result = {
            'status': 'skipped',
            'reason': None,
            'model': 'Qari-OCR-via-RunPod',
            'ocr_text': None,
        }

        try:
            qari_result['status'] = 'attempted'
            print(f'Processing {len(image_paths)} images with Qari OCR')

            # Process all images concurrently using the existing single image logic
            async def process_image_async(image_path: str, page_num: int):
                """Process a single image asynchronously using existing logic."""
                try:
                    # Use the existing single image processing logic
                    result = TransductionTaskFileActions._process_single_image_with_qari(
                        image_path,
                        'png',
                        cancel_checker=cancel_checker,
                        register_job_fn=register_job_fn,
                    )
                    if result['status'] == 'completed':
                        cleaned_text = _clean_qari_ocr_html_preserve_breaks(result['ocr_text'] or '')
                        return {'page': page_num, 'status': 'completed', 'text': cleaned_text, 'model': result['model']}
                    else:
                        return {'page': page_num, 'status': 'failed', 'reason': result['reason'], 'text': None}
                except Exception as e:
                    return {'page': page_num, 'status': 'failed', 'reason': str(e), 'text': None}

            # Process all images concurrently
            async def process_all_images():
                tasks = []
                for i, image_path in enumerate(image_paths):
                    task = process_image_async(image_path, i)
                    tasks.append(task)
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                return results

            # Run the async processing
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(process_all_images())
            
            # Process results and stitch text together
            successful_results = []
            failed_results = []
            
            for result in results:
                if isinstance(result, dict) and result.get('status') == 'completed' and result.get('text'):
                    successful_results.append(result)
                else:
                    failed_results.append(result)
            
            # Print the full image paths
            print('Image paths:', image_paths)
            # # Clean up temporary image files
            # for image_path in image_paths:
            #     try:
            #         os.remove(image_path)
            #         print(f'Cleaned up temporary image: {image_path}')
            #     except Exception as e:
            #         print(f'Failed to clean up {image_path}: {e}')
            
            if successful_results:
                # Sort by page number to maintain order
                successful_results.sort(key=lambda x: x['page'])
                
                # Stitch text together with page separators
                ocr_texts = []
                for result in successful_results:
                    page_text = f"[Page {result['page'] + 1}]\n{result['text']}"
                    ocr_texts.append(page_text)
                
                qari_result['status'] = 'completed'
                qari_result['ocr_text'] = '\n\n'.join(ocr_texts)
                qari_result['model'] = successful_results[0].get('model', 'Qari-OCR-via-RunPod')
                
                if failed_results:
                    print(f'Warning: {len(failed_results)} pages failed to process')
                
                print(f'PDF OCR completed successfully for {len(successful_results)} pages')
                return qari_result
            else:
                qari_result['status'] = 'failed'
                qari_result['reason'] = 'All PDF pages failed to process'
                print(f'All PDF pages failed to process')
                return qari_result

        except Exception as e:
            qari_result['status'] = 'failed'
            qari_result['reason'] = f'PDF processing error: {e.__class__.__name__}: {e}'
            print(f'PDF processing error: {e.__class__.__name__}: {e}')
            
            # Clean up temporary image files on error
            print('Cleaning up temporary image files on error...')
            for image_path in image_paths:
                try:
                    os.remove(image_path)
                    print(f'Cleaned up temporary image on error: {image_path}')
                except Exception as cleanup_error:
                    print(f'Failed to clean up {image_path} on error: {cleanup_error}')
            
            return qari_result

    @staticmethod
    def upload_file(request: FastAPIRequest, file: UploadFile, db_session: Session):
        if not file.filename:
            raise InvalidRequestData(
                message='File name is required',
            )

        if not file.content_type:
            raise InvalidRequestData(
                message='File content type is required',
            )

        # Only accept jpeg, png, jpg
        if file.content_type not in ('image/jpeg', 'image/png', 'image/jpg', 'application/pdf'):
            raise InvalidRequestData(
                message='File must be a jpeg, png, jpg, or pdf',
            )

        # Determine file size from request headers or file object
        content_length = None
        # Try framework-specific attribute first (e.g., Flask)
        if hasattr(request, 'content_length') and request.content_length:
            content_length = request.content_length
        # Try FastAPI/Starlette headers
        if not content_length and hasattr(request, 'headers') and request.headers:
            cl_header = request.headers.get('content-length') or request.headers.get('Content-Length')
            if cl_header:
                try:
                    content_length = int(cl_header)
                except Exception:
                    content_length = None
        # Fallback: compute from file stream
        if not content_length:
            try:
                file_obj = getattr(file, 'file', None) or file
                current_pos = file_obj.tell()
                file_obj.seek(0, os.SEEK_END)
                content_length = file_obj.tell()
                file_obj.seek(current_pos, os.SEEK_SET)
            except Exception:
                content_length = None
        if not content_length:
            raise InvalidRequestData(
                message='Could not determine file size',
            )

        # Check if the file is too large
        if content_length > 30 * 1024 * 1024:
            raise InvalidRequestData(
                message='File must be less than 30MB',
            )

        # Check if the file is too small
        if content_length < 1024:
            raise InvalidRequestData(
                message='File must be greater than 1KB',
            )

        # Flatten the file name and append a timestamp
        file_name = f"transduction_task_file_{uuid.uuid4()}"

        # Get the file extension
        file_extension = os.path.splitext(file.filename)[1]

        # Add the extension to the file name
        file_name = f'{file_name}{file_extension}'

        uploads_dir = 'uploads'
        # # Ensure uploads directory exists
        # if not os.path.exists(uploads_dir):
        #     os.makedirs(uploads_dir, exist_ok=True)

        dest_path = os.path.join(uploads_dir, file_name)

        # FastAPI/Starlette UploadFile exposes an underlying file-like object
        file_stream = getattr(file, 'file', None) or getattr(file, 'stream', None)
        if not file_stream:
            raise InvalidRequestData(
                message='Could not access file stream',
            )
        try:
            file_stream.seek(0, os.SEEK_SET)
        except Exception:
            pass

        with open(dest_path, 'wb') as out_file:
            print(f'Writing file to {dest_path}...')
            while True:
                chunk = file_stream.read(1024 * 1024)
                if not chunk:
                    break
                out_file.write(chunk)

        # Determine file_type expected by model (pdf/png/jpg)
        content_type_map = {
            'application/pdf': 'pdf',
            'image/png': 'png',
            'image/jpeg': 'jpg',
            'image/jpg': 'jpg',
        }
        file_type = content_type_map.get(file.content_type)
        if not file_type:
            ext = (file_extension or '').lower().lstrip('.')
            if ext in ('jpeg', 'jpg'):
                file_type = 'jpg'
            elif ext in ('png',):
                file_type = 'png'
            elif ext in ('pdf',):
                file_type = 'pdf'
            else:
                raise InvalidRequestData(
                    message='Unsupported file type',
                )

        # Create DB row for TransductionTaskFile only (no OCR/translation here)
        new_record = TransductionTaskFile(
            id_transduction_task=None,
            file_name=file.filename,
            file_path=dest_path,
            file_type=file_type,
        )
        db_session.add(new_record)
        db_session.flush()

        return new_record.to_dict()

    @staticmethod
    def generate_docx_file(translation_text=None, transliteration_text=None, original_text=None, new_record=None):
        doc = Document()
        heading = doc.add_heading('Translated Content', level=1)

        # Change line spacing for the "Normal" style
        style = doc.styles['Normal']
        paragraph_format = style.paragraph_format
        paragraph_format.line_spacing = Pt(24)   # roughly 1.5–2x spacing

        # Make it bigger
        run = heading.runs[0]
        run.font.size = Pt(28)   # 28pt is larger than default heading size

        # Center align the whole paragraph
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # # Add a line break
        # p = doc.add_paragraph()
        # p.add_run().add_break()
        
        # Add the translated text (page-wise if markers are present)
        text = translation_text
        if text is None and new_record is not None:
            # Backward compatibility if called with record
            text = ((new_record.meta or {}).get('openai') or {}).get('translation')

        if text:
            # Parse page markers like [Page N]\n...
            tx_page_nums = re.findall(r"\[Page (\d+)\]", text)
            tx_splits = re.split(r"\[Page \d+\]\s*\n?", text)
            tx_page_chunks = []
            if tx_page_nums:
                tx_chunks = tx_splits[1:] if len(tx_splits) > 1 else []
                for i, chunk in enumerate(tx_chunks):
                    try:
                        n = int(tx_page_nums[i])
                    except Exception:
                        n = i + 1
                    tx_page_chunks.append((n, chunk.strip()))
            else:
                tx_page_chunks.append((1, text.strip()))

            for page_num, chunk in tx_page_chunks:
                sub = doc.add_heading(f'Page {page_num}', level=2)
                sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
                doc.add_paragraph(chunk)
        else:
            doc.add_paragraph('')

        # Add transliteration section if available
        try:
            tr_text = transliteration_text
            if tr_text is None and new_record is not None:
                tr_text = (((new_record.meta or {}).get('transliteration') or {}).get('transliteration'))

            if tr_text:
                doc.add_page_break()
                tr_heading = doc.add_heading('Transliteration', level=1)
                style = doc.styles['Normal']
                paragraph_format = style.paragraph_format
                paragraph_format.line_spacing = Pt(24)

                run = tr_heading.runs[0]
                run.font.size = Pt(28)
                tr_heading.alignment = WD_ALIGN_PARAGRAPH.LEFT

                tr_page_nums = re.findall(r"\[Page (\d+)\]", tr_text)
                tr_splits = re.split(r"\[Page \d+\]\s*\n?", tr_text)
                tr_page_chunks = []
                if tr_page_nums:
                    tr_chunks = tr_splits[1:] if len(tr_splits) > 1 else []
                    for i, chunk in enumerate(tr_chunks):
                        try:
                            n = int(tr_page_nums[i])
                        except Exception:
                            n = i + 1
                        tr_page_chunks.append((n, (chunk or '').strip()))
                else:
                    tr_page_chunks.append((1, (tr_text or '').strip()))

                for page_num, chunk in tr_page_chunks:
                    sub = doc.add_heading(f'Page {page_num}', level=2)
                    sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for line in (chunk or '').splitlines():
                        if not line.strip():
                            continue
                        p = doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        p.add_run(line)
        except Exception:
            pass

        # Add original Arabic content page-wise if available
        try:
            original = original_text
            if original is None and new_record is not None:
                # Try to fetch from record meta if not provided
                original = (((new_record.meta or {}).get('ocr') or {}).get('ocr_text'))

            if original:
                doc.add_page_break()
                ar_heading = doc.add_heading('Original Content', level=1)
                style = doc.styles['Normal']
                paragraph_format = style.paragraph_format
                paragraph_format.line_spacing = Pt(12)   # roughly 1.5–2x spacing

                # Make it bigger
                run = ar_heading.runs[0]
                run.font.size = Pt(28)   # 28pt is larger than default heading size

                ar_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # Parse page markers like [Page N]\n...
                page_nums = re.findall(r"\[Page (\d+)\]", original)
                splits = re.split(r"\[Page \d+\]\s*\n?", original)
                # re.split returns first chunk before first marker at index 0
                # Pair page numbers with corresponding text chunks
                page_chunks = []
                if page_nums:
                    # Ignore leading preface if empty
                    chunks = splits[1:] if len(splits) > 1 else []
                    for i, chunk in enumerate(chunks):
                        try:
                            n = int(page_nums[i])
                        except Exception:
                            n = i + 1
                        page_chunks.append((n, chunk.strip()))
                else:
                    # No markers; treat as single page
                    page_chunks.append((1, original.strip()))

                for page_num, chunk in page_chunks:
                    # Page heading (RTL)
                    sub = doc.add_heading(f'Page {page_num}', level=2)
                    sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    try:
                        sub_pPr = sub._p.get_or_add_pPr()
                        sub_bidi = OxmlElement('w:bidi')
                        sub_bidi.set(qn('w:val'), '1')
                        sub_pPr.append(sub_bidi)
                    except Exception:
                        pass

                    # One paragraph per line, enforced RTL
                    for line in (chunk or '').splitlines():
                        if not line.strip():
                            continue
                        p = doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        try:
                            p.paragraph_format.left_indent = None
                            p.paragraph_format.right_indent = None
                            p.paragraph_format.first_line_indent = None
                        except Exception:
                            pass
                        try:
                            pPr = p._p.get_or_add_pPr()
                            bidi = OxmlElement('w:bidi')
                            bidi.set(qn('w:val'), '1')
                            pPr.append(bidi)
                        except Exception:
                            pass
                        run = p.add_run('\u061C' + line)
                        try:
                            rPr = run._r.get_or_add_rPr()
                            rtl = OxmlElement('w:rtl')
                            rtl.set(qn('w:val'), '1')
                            rPr.append(rtl)
                            lang = OxmlElement('w:lang')
                            lang.set(qn('w:bidi'), 'ar-SA')
                            rPr.append(lang)
                        except Exception:
                            pass
        except Exception:
            # Best-effort; if anything fails, still return a valid docx with translation
            pass
        file_path = os.path.join(
            'uploads',
            f'{str(uuid.uuid4())}.docx',
        )
        doc.save(file_path)
        return file_path

    @staticmethod
    def translate_text_with_openai(arabic_text: str):
        """
        Translate Arabic text to English using OpenAI's Chat Completions.

        Returns a dict: {
            'status': 'skipped'|'attempted'|'completed'|'failed',
            'reason': str|None,
            'model': str|None,
            'translation': str|None,
        }
        """
        result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'translation': None,
        }

        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_TRANSLATION_MODEL', 'gpt-4o-mini')
        if not api_key:
            result['reason'] = 'OPENAI_API_KEY not set'
            return result

        try:
            # Prefer the official openai package v1+ style client
            client = OpenAI(api_key=api_key)
            result['status'] = 'attempted'
            result['model'] = model

            prompt_system = 'You are a translation engine. Translate Arabic to English. Return only the English translation, no extra text. Do not add any other text or comments. Do not just summarize. Translate the whole text line by line. Important: Keep any page markers of the form [Page N] EXACTLY as-is, on their own lines, without translation, removal, renumbering, or reformatting.'
            messages = [
                { 'role': 'system', 'content': prompt_system },
                { 'role': 'user', 'content': arabic_text },
            ]
            resp = client.chat.completions.create(model=model, messages=messages)
            if getattr(resp, 'choices', None) and len(resp.choices) > 0:
                msg = resp.choices[0].message
                content = getattr(msg, 'content', None) if msg else None
                if content:
                    result['status'] = 'completed'
                    result['translation'] = content
                else:
                    result['status'] = 'failed'
                    result['reason'] = 'No content in OpenAI response'
            else:
                result['status'] = 'failed'
                result['reason'] = 'Empty OpenAI response'
        except Exception as e:
            result['status'] = 'failed'
            result['reason'] = f'OpenAI error: {e.__class__.__name__}: {e}'

        return result

    @staticmethod
    def transliterate_text_with_openai(arabic_text: str):
        """
        Transliterate Arabic text to Latin script using OpenAI, preserving line structure and page markers.

        Returns a dict: {
            'status': 'skipped'|'attempted'|'completed'|'failed',
            'reason': str|None,
            'model': str|None,
            'transliteration': str|None,
        }
        """

        result = {
            'status': 'skipped',
            'reason': None,
            'model': None,
            'transliteration': None,
        }

        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_TRANSLITERATION_MODEL', os.getenv('OPENAI_TRANSLATION_MODEL', 'gpt-4o-mini'))
        if not api_key:
            result['reason'] = 'OPENAI_API_KEY not set'
            return result

        try:
            client = OpenAI(api_key=api_key)
            result['status'] = 'attempted'
            result['model'] = model

            base_prompt = (
                'Transliterate the following Arabic text into Latin script using standard Arabic phonetic transliteration. '
                'Use macrons for long vowels (ā, ī, ū), dots for emphatic consonants (ṣ, ḍ, ṭ, ẓ), and special signs for ʿ (ʿayn) and \' (hamzah). '
                'Apply assimilation rules for the definite article (al → aḍ, as, etc.) when followed by sun letters. '
                'Replace any occurrence of ’l with l. Keep the line structure of the original text.'
            )

            extra_constraints = (
                'Important instructions: '
                '1) Preserve any page markers exactly as-is, e.g., [Page N], on their own lines. Do not translate, remove, or reformat page markers. '
                '2) Preserve original line breaks and paragraph structure one-to-one. '
                '3) Return only the transliteration text, with no extra commentary.'
            )

            prompt_system = f'{base_prompt} {extra_constraints}'
            messages = [
                { 'role': 'system', 'content': prompt_system },
                { 'role': 'user', 'content': arabic_text },
            ]

            resp = client.chat.completions.create(model=model, messages=messages)
            if getattr(resp, 'choices', None) and len(resp.choices) > 0:
                msg = resp.choices[0].message
                content = getattr(msg, 'content', None) if msg else None
                if content:
                    result['status'] = 'completed'
                    result['transliteration'] = content
                else:
                    result['status'] = 'failed'
                    result['reason'] = 'No content in OpenAI response'
            else:
                result['status'] = 'failed'
                result['reason'] = 'Empty OpenAI response'
        except Exception as e:
            result['status'] = 'failed'
            result['reason'] = f'OpenAI error: {e.__class__.__name__}: {e}'

        return result
