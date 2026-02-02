import os
import jwt
import json
import logging

from typing import Annotated, Optional
from functools import partial
from fastapi import (
    FastAPI,
    Depends,
    Query,
    Path,
    UploadFile,
    File,
    Request,
    HTTPException,
)
from fastapi.security import OAuth2PasswordBearer

from backend.meta.pydantic_type_generator import generate_pydantic_model
from backend.pydantic_types import (
    PaginationParams,
)
from backend.actions import (
    DynamicActions,
    MetadataActions,
)
from backend.database import get_db, commit_db_session, SessionLocal
from backend.models import *
from backend.helpers import responsify, parse_request_params
from backend.database import get_db
from backend.responses import (
    get_buyers_response,
    get_buyer_detail_response,
    get_buyer_disputes_response,
    REVENUE_TREND_RESPONSE,
    REVENUE_TYPE_RESPONSE,
    TOP_DISPUTE_REASONS_RESPONSE,
    TOP_CATEGORIES_BY_PURCHASE_RESPONSE,
    RETURNING_VS_NEW_USERS_RESPONSE,
    VISITOR_STATUS_RESPONSE,
    DISPUTE_INSIGHTS_RESPONSE,
    COMPLIANCE_BREAKDOWN_RESPONSE,
    COMPLIANCE_ISSUE_TYPES_RESPONSE,
    API_CHECK_TREND_RESPONSE,
    TOP_API_ERROR_TYPES_RESPONSE,
    LEAD_DELIVERY_TREND_RESPONSE,
    TOP_BUYERS_BY_SPEND_RESPONSE,
    TOP_SELLERS_BY_REVENUE_RESPONSE,
    VISITOR_ACTIVITY_TREND_RESPONSE,
    USER_ACTIVITY_TREND_RESPONSE,
)

# Import exception handlers
from backend.middleware import register_exception_handlers

# Create FastAPI app
app = FastAPI(
    title='TDS Corporate API',
    description='Backend API for TDS Corporate Website',
    version='1.0.0',
)

# Optional OAuth2 bearer for endpoints that can accept a token if present
oauth2_optional = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
oauth2_required = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)


logger = logging.getLogger(__name__)

# Register all exception handlers
register_exception_handlers(app)


ADMIN_API_PREFIX = '/api/v1/admin'


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {"status": "healthy", "service": "tds-corporate-api"}


class MetadataObjectRoutes:
    @app.get(
        '/api/v1/admin/metadata-objects',
        operation_id='get_all_metadata_objects',
        summary='Get all metadata objects',
        description='Retrieve a paginated list of all metadata objects',
        tags=['Metadata Object']
    )
    def get_all_metadata_objects(
        pagination_params: Annotated[PaginationParams, Query()],
        db_session=Depends(get_db),
    ):
        metadata_objects, pagination = MetadataActions.get_all_metadata_objects(
            db_session=db_session,
            pagination=pagination_params.model_dump(),
        )
        return responsify(
            (
                metadata_objects,
                pagination,
            ),
        )


def create_route_handler(route_type, metadata_object, metadata_fields, model_class):
    """
    Create a route handler with proper parameter handling.
    """

    name = metadata_object.api_configuration['name']
    singular = metadata_object.api_configuration['singular']
    plural = metadata_object.api_configuration['plural']
    plural_kebab = metadata_object.api_configuration['plural'].replace('_', '-')
    param_name = f'id_{singular}'
    
    if route_type == 'get_all':
        @app.get(
            f'/api/v1/admin/{plural_kebab}',
            operation_id=f'get_all_{name}',
            summary=f'Get all {plural}',
            description=f'''Retrieve a paginated list of all {plural}.

**Filter Parameters:**
Use `f_fieldname=value` format for filtering:
- `f_fieldname=value` - Exact match
- `f_fieldname=~value` - Contains text (case-insensitive)
- `f_fieldname=>value` - Greater than (numbers/dates)
- `f_fieldname=<value` - Less than (numbers/dates)

**Examples:**
- `f_status=active` - Filter by status
- `f_name=~electronics` - Names containing "electronics"
- `f_name=^tech` - Names starting with "tech"
- `f_id=>10` - IDs greater than 10
''',
            tags=[name]
        )
        def handler(
            request: Request,
            db_session=Depends(get_db),
            
            # Pagination parameters
            page: Annotated[Optional[int], Query(description="Page number (starting from 1)", ge=1)] = 1,
            page_size: Annotated[Optional[int], Query(description="Number of items per page", ge=1, le=1000)] = 100,
            
            # Search and sorting
            q: Annotated[Optional[str], Query(description="Global search query across searchable fields")] = None,
            sort_by: Annotated[Optional[str], Query(description="Sort by field name. Use '-' prefix for descending (e.g., '-name')")] = None,
        ):
            # Parse query parameters from request (including dynamic f_ filters)
            request_args = dict(request.query_params)
            parsed_params = parse_request_params(
                request_args=request_args,
                main_model_class=model_class,
                secondary_models_map={}
            )
            
            method = getattr(DynamicActions, 'get_all')
            items_details, pagination = method(
                model_class=model_class,
                db_session=db_session,
                filters=parsed_params['filters'],
                sort_details=parsed_params['sort_details'],
                q=parsed_params['q'],
                secondary_models_map=parsed_params['secondary_models_map'],
                pagination=parsed_params['pagination'],
            )
            return responsify(
                (
                    items_details,
                    pagination,
                ),
            )
        handler.__name__ = f'get_all_{name}'
        return handler
        
    elif route_type == 'get_one':
        @app.get(
            f'/api/v1/admin/{plural_kebab}/{{{param_name}}}',
            operation_id=f'get_one_{name}',
            summary=f'Get {singular} by ID',
            description=f'Retrieve a specific {singular} by their ID',
            tags=[name]
        )
        def handler(
            id_param: int = Path(..., alias=param_name),
            db_session=Depends(get_db)
        ):
            method = getattr(DynamicActions, 'get_one')
            item_details = method(
                model_class=model_class,
                id_item=id_param,
                db_session=db_session
            )
            return responsify(
                item_details,
            )
        handler.__name__ = f'get_one_{name}'
        return handler
        
    elif route_type == 'post':
        pydantic_create_model = generate_pydantic_model(
            object=metadata_object,
            fields=metadata_fields,
            model_type='create',
        )
        status_code = 201

        @app.post(
            f'/api/v1/admin/{plural_kebab}',
            operation_id=f'create_{name}',
            summary=f'Create {singular}',
            description=f'Create a new {singular}',
            tags=[name],
            status_code=status_code,
        )
        def handler(
            data_model: pydantic_create_model,
            db_session=Depends(commit_db_session),
        ):
            method = getattr(DynamicActions, 'create')
            item_details = method(
                model_class=model_class,
                data=data_model.model_dump(),
                db_session=db_session,
            )
            return responsify(
                item_details,
                status_code=status_code,
            )
        handler.__name__ = f'create_{name}'
        return handler
        
    elif route_type == 'patch':
        pydantic_update_model = generate_pydantic_model(
            object=metadata_object,
            fields=metadata_fields,
            model_type='update',
        )

        @app.patch(
            f'/api/v1/admin/{plural_kebab}/{{{param_name}}}',
            operation_id=f'update_{name}',
            summary=f'Update {singular}',
            description=f'Update an existing {singular} by their ID',
            tags=[name]
        )
        def handler(
            data: pydantic_update_model,
            id_param: int = Path(..., alias=param_name),
            db_session=Depends(commit_db_session),
        ):
            method = getattr(DynamicActions, 'update')
            item_details = method(
                model_class=model_class,
                **{param_name: id_param},
                data=data,
                db_session=db_session,
            )
            return responsify(
                item_details,
            )
        handler.__name__ = f'update_{name}'
        return handler
        
    elif route_type == 'delete':
        @app.delete(
            f'/api/v1/admin/{plural_kebab}/{{{param_name}}}',
            operation_id=f'delete_{name}',
            summary=f'Delete {singular}',
            description=f'Delete a {singular} by their ID',
            tags=[name]
        )
        def handler(
            id_param: int = Path(..., alias=param_name),
            db_session=Depends(commit_db_session),
        ):
            method = getattr(DynamicActions, 'delete')
            details = method(
                model_class=model_class,
                **{param_name: id_param},
                db_session=db_session,
            )
            return responsify(
                details,
            )
        handler.__name__ = f'delete_{name}'
        return handler



def generate_routes_from_metadata_objects():
    """
    Dynamically generate routes from metadata_objects configuration.
    """

    db_session = SessionLocal()
    try:
        metadata_objects = MetadataObject.get_items(
            db_session=db_session,
        )

        for metadata_object in metadata_objects:
            if not metadata_object.api_configuration.get('is_enabled'):
                print(f'Skipping {metadata_object.name} APIs because it is not enabled')
                continue

            metadata_fields = MetadataField.get_items(
                db_session=db_session,
                filters=[{
                    'field': 'id_metadata_object',
                    'model': MetadataField,
                    'equal_to': metadata_object.id,
                }],
            )

            model_class = globals()[metadata_object.api_configuration['class_name']]

            # Generate routes based on configuration
            for route_type in metadata_object.api_configuration['routes']:
                create_route_handler(
                    route_type,
                    metadata_object,
                    metadata_fields,
                    model_class,
                )
    finally:
        db_session.close()


# Generate routes dynamically
try:
    generate_routes_from_metadata_objects()
except Exception as e:
    logger.warning(f"Could not generate dynamic routes on startup: {e}")
    logger.info("Routes will be generated when database is available")


# @app.get(f'{ADMIN_API_PREFIX}/buyers')
def list_buyers(
    page: int = Query(default=1, ge=1, description='Page number for buyers list pagination'),
    page_size: int = Query(
        default=100,
        ge=1,
        le=500,
        description='Number of buyers to return per page',
    ),
):
    """Return a static list of buyers for initial wiring."""
    return get_buyers_response(page=page, page_size=page_size)


# @app.get(f'{ADMIN_API_PREFIX}/buyers/{{buyer_id}}')
def get_buyer_detail(
    buyer_id: int = Path(..., ge=1, description='Buyer identifier'),
):
    """Return hard-coded buyer details for the admin preview."""
    response = get_buyer_detail_response(buyer_id=buyer_id)
    if response is None:
        raise HTTPException(status_code=404, detail='Buyer not found')
    return response


# @app.get(f'{ADMIN_API_PREFIX}/buyers/{{buyer_id}}/disputes')
def list_buyer_disputes(
    buyer_id: int = Path(..., ge=1, description='Buyer identifier'),
    page: int = Query(default=1, ge=1, description='Page number for buyer disputes pagination'),
    page_size: int = Query(
        default=50,
        ge=1,
        le=500,
        description='Number of dispute records to return per page',
    ),
):
    """Return hard-coded disputes for the specified buyer."""
    response = get_buyer_disputes_response(buyer_id=buyer_id, page=page, page_size=page_size)
    if response is None:
        raise HTTPException(status_code=404, detail='Buyer not found')
    return response


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/revenue-trend',
    operation_id='get_dashboard_revenue_trend',
    summary='Get revenue trend data',
    description='Return hard-coded revenue totals for dashboard trend visualisations.',
    tags=['Dashboard'],
)
def get_dashboard_revenue_trend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static revenue trend data for the dashboard."""
    return REVENUE_TREND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/revenue-type',
    operation_id='get_dashboard_revenue_type',
    summary='Get revenue type breakdown',
    description='Return hard-coded revenue totals by portal for dashboard visualisations.',
    tags=['Dashboard'],
)
def get_dashboard_revenue_type(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static revenue breakdown by type for the dashboard."""
    return REVENUE_TYPE_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/top-dispute-reasons',
    operation_id='get_dashboard_top_dispute_reasons',
    summary='Get top dispute reasons',
    description='Return hard-coded dispute counts by reason for dashboard charts.',
    tags=['Dashboard'],
)
def get_dashboard_top_dispute_reasons(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static top dispute reasons for the dashboard."""
    return TOP_DISPUTE_REASONS_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/top-categories-by-purchase',
    operation_id='get_dashboard_top_categories_by_purchase',
    summary='Get top categories by purchase volume',
    description='Return hard-coded purchase counts per category for dashboard visualisations.',
    tags=['Dashboard'],
)
def get_dashboard_top_categories_by_purchase(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static top purchase categories for the dashboard."""
    return TOP_CATEGORIES_BY_PURCHASE_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/dispute-insights',
    operation_id='get_dashboard_dispute_insights',
    summary='Get dispute insights summary',
    description='Return hard-coded dispute status, reasons, and GDPR fine counts for dashboards.',
    tags=['Dashboard'],
)
def get_dashboard_dispute_insights(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static dispute insights for the dashboard."""
    return DISPUTE_INSIGHTS_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/compliance-breakdown',
    operation_id='get_dashboard_compliance_breakdown',
    summary='Get compliance breakdown',
    description='Return hard-coded compliance counts by verification outcome for dashboard visuals.',
    tags=['Dashboard'],
)
def get_dashboard_compliance_breakdown(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static compliance breakdown data for the dashboard."""
    return COMPLIANCE_BREAKDOWN_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/compliance-issue-types',
    operation_id='get_dashboard_compliance_issue_types',
    summary='Get compliance issue types by day',
    description='Return hard-coded daily compliance issue counts by reason for dashboard charts.',
    tags=['Dashboard'],
)
def get_dashboard_compliance_issue_types(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static daily compliance issue types for the dashboard."""
    return COMPLIANCE_ISSUE_TYPES_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/api-check-trend',
    operation_id='get_dashboard_api_check_trend',
    summary='Get API check trend data',
    description='Return hard-coded API check counts per day for dashboard trend charts.',
    tags=['Dashboard'],
)
def get_dashboard_api_check_trend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static API check trend data for the dashboard."""
    return API_CHECK_TREND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/top-api-error-types',
    operation_id='get_dashboard_top_api_error_types',
    summary='Get top API error types',
    description='Return hard-coded API error counts aggregated by type for dashboards.',
    tags=['Dashboard'],
)
def get_dashboard_top_api_error_types(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static top API error types for the dashboard."""
    return TOP_API_ERROR_TYPES_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/lead-delivery-trend',
    operation_id='get_dashboard_lead_delivery_trend',
    summary='Get lead delivery trend data',
    description='Return hard-coded lead delivery counts per day for dashboard trend charts.',
    tags=['Dashboard'],
)
def get_dashboard_lead_delivery_trend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static lead delivery trend data for the dashboard."""
    return LEAD_DELIVERY_TREND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/top-buyers-by-spend',
    operation_id='get_dashboard_top_buyers_by_spend',
    summary='Get top buyers by spend',
    description='Return hard-coded buyer totals including spend and purchase/dispute counts.',
    tags=['Dashboard'],
)
def get_dashboard_top_buyers_by_spend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static top buyers by spend for the dashboard."""
    return TOP_BUYERS_BY_SPEND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/top-sellers-by-revenue',
    operation_id='get_dashboard_top_sellers_by_revenue',
    summary='Get top sellers by revenue',
    description='Return hard-coded seller totals including revenue and dispute counts.',
    tags=['Dashboard'],
)
def get_dashboard_top_sellers_by_revenue(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static top sellers by revenue for the dashboard."""
    return TOP_SELLERS_BY_REVENUE_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/visitor-activity-trend',
    operation_id='get_dashboard_visitor_activity_trend',
    summary='Get visitor activity trend',
    description='Return hard-coded hourly visitor activity scores for each day.',
    tags=['Dashboard'],
)
def get_dashboard_visitor_activity_trend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static visitor activity trend data for the dashboard."""
    return VISITOR_ACTIVITY_TREND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/user-activity-trend',
    operation_id='get_dashboard_user_activity_trend',
    summary='Get user activity trend',
    description='Return hard-coded hourly user activity scores for each day.',
    tags=['Dashboard'],
)
def get_dashboard_user_activity_trend(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static user activity trend data for the dashboard."""
    return USER_ACTIVITY_TREND_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/returning-vs-new-users',
    operation_id='get_dashboard_returning_vs_new_users',
    summary='Get returning vs new user counts',
    description='Return hard-coded totals for overall, new, and returning users.',
    tags=['Dashboard'],
)
def get_dashboard_returning_vs_new_users(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static returning vs new user metrics for the dashboard."""
    return RETURNING_VS_NEW_USERS_RESPONSE


@app.get(
    f'{ADMIN_API_PREFIX}/dashboard/visitor-status',
    operation_id='get_dashboard_visitor_status',
    summary='Get visitor status breakdowns',
    description='Return hard-coded buyer/seller status metrics and verification split.',
    tags=['Dashboard'],
)
def get_dashboard_visitor_status(
    start_date: Annotated[Optional[str], Query(alias='startDate', description='Start date filter (ISO format)')] = None,
    end_date: Annotated[Optional[str], Query(alias='endDate', description='End date filter (ISO format)')] = None,
):
    """Return static visitor status data for the dashboard."""
    return VISITOR_STATUS_RESPONSE


@app.post(
    '/api/v1/upload',
    operation_id='upload_file',
    summary='Upload File',
    description='Generic file upload endpoint. Stores file under uploads/ and returns metadata.',
    tags=['File']
)
def upload_file_endpoint(file: UploadFile = File(...), db_session=Depends(get_db)):
    from backend.actions import BackgroundJobActions  # avoid circular
    # Implement upload directly to avoid pulling transduction-specific code
    import os, uuid

    if not file.filename:
        return responsify({'error': 'File name is required'}, status_code=422)

    uploads_dir = 'uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    stored_name = f"upload_{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    dest_path = os.path.join(uploads_dir, stored_name)

    file_stream = getattr(file, 'file', None) or getattr(file, 'stream', None)
    if not file_stream:
        return responsify({'error': 'Could not access file stream'}, status_code=422)

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

    return responsify({
        'file_name': file.filename,
        'stored_name': stored_name,
        'path': dest_path,
    })
