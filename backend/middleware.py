import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from backend.exceptions import (
    Forbidden,
    Unauthorized,
    ResourceNotFound,
    InvalidRequestData,
    InternalServerError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    """
    Register all exception handlers for the FastAPI app
    """
    
    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(request: Request, exc: RequestValidationError):
        """
        Handle FastAPI request validation errors
        """

        logger.warning(f"Request validation error in {request.url.path}: {exc}")
        
        # Convert FastAPI validation errors to our format
        errors = []
        for error in exc.errors():
            error_dict = {
                # 'body' is the first element of the loc tuple
                'field': '.'.join(str(loc) for loc in error['loc'][1:]),
                'description': error['msg'],
            }
            errors.append(error_dict)
        
        error_response = {
            'status': 'error',
            'errors': errors,
            'message': 'Validation failed',
        }
        
        return JSONResponse(
            status_code=422,
            content=error_response
        )
    
    @app.exception_handler(InvalidRequestData)
    async def handle_invalid_request_data(request: Request, exc: InvalidRequestData):
        """Handle InvalidRequestData exceptions"""
        status_code = getattr(exc, 'http_status', 400)
        detail = getattr(exc, 'message', str(exc))
        logger.warning(f'InvalidRequestData in {request.url.path}: {detail}')
        
        # Use actual errors from exception if available
        if hasattr(exc, 'errors') and exc.errors:
            # Ensure all errors have the 'type' field
            errors = []
            for error in exc.errors:
                error_dict = error.copy()
                if 'type' not in error_dict:
                    error_dict['type'] = 'validation_error'
                errors.append(error_dict)
        else:
            errors = []
        
        error_response = {
            'status': 'error',
            'errors': errors,
            'message': detail,
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    @app.exception_handler(Unauthorized)
    async def handle_unauthorized(request: Request, exc: Unauthorized):
        """Handle Unauthorized exceptions"""
        status_code = getattr(exc, 'http_status', 401)
        detail = getattr(exc, 'message', str(exc))
        logger.warning(f'Unauthorized in {request.url.path}: {detail}')
        
        error_response = {
            'status': 'error',
            'errors': [],
            'message': detail,
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    @app.exception_handler(Forbidden)
    async def handle_forbidden(request: Request, exc: Forbidden):
        """Handle Forbidden exceptions"""
        status_code = getattr(exc, 'http_status', 403)
        detail = getattr(exc, 'message', str(exc))
        logger.warning(f'Forbidden in {request.url.path}: {detail}')
        
        error_response = {
            'status': 'error',
            'errors': [],
            'message': detail,
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    @app.exception_handler(ResourceNotFound)
    async def handle_resource_not_found(request: Request, exc: ResourceNotFound):
        """Handle ResourceNotFound exceptions"""
        status_code = getattr(exc, 'http_status', 404)
        detail = getattr(exc, 'message', str(exc))
        logger.warning(f'ResourceNotFound in {request.url.path}: {detail}')
        
        error_response = {
            'status': 'error',
            'errors': [],
            'message': detail,
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    @app.exception_handler(InternalServerError)
    async def handle_internal_server_error(request: Request, exc: InternalServerError):
        """Handle InternalServerError exceptions"""
        status_code = getattr(exc, 'http_status', 500)
        detail = getattr(exc, 'message', str(exc))
        logger.error(f'InternalServerError in {request.url.path}: {detail}')
        
        error_response = {
            'status': 'error',
            'errors': [],
            'message': detail,
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        """Handle all other unexpected exceptions"""
        logger.error(f'Unexpected error in {request.url.path}: {str(exc)}', exc_info=True)
        
        error_response = {
            'status': 'error',
            'errors': [],
            'message': 'Internal server error',
        }
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )

