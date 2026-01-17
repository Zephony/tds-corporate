from sqlalchemy import Column, Integer, String
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class DisputeInsightsReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'dispute_insights_reports'

    # Type of metric (dispute_status, dispute_reasons, gdpr_fines)
    metric_type = Column(String(50), info={
        'display_name': 'Metric Type',
        'description': 'Type of dispute metric',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
    })

    # Category within the metric (active, solved, closed, payment_issue, etc.)
    metric_category = Column(String(50), info={
        'display_name': 'Metric Category',
        'description': 'Category within the metric type',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
    })

    # Count for this category
    count = Column(Integer, info={
        'display_name': 'Count',
        'description': 'Count/number for this category',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_filterable': True,
        'is_sortable': True,
    })

    # For seller-specific data (null for aggregated)
    id_seller = Column(Integer, info={
        'display_name': 'Seller ID',
        'description': 'Seller ID for seller-specific data (null for aggregated)',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_filterable': True,
    })

    # Define readable and updateable fields
    readable_fields = [
        'id', 'metric_type', 'metric_category', 'count', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'metric_type', 'metric_category', 'count', 'id_seller'
    ]

    searchable_fields = [
        'metric_type', 'metric_category'
    ]
