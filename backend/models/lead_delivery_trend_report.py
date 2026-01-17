from sqlalchemy import Column, String, Integer, Date
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class LeadDeliveryTrendReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'lead_delivery_trend_reports'

    # Date for this data point
    date = Column(Date, info={
        'display_name': 'Date',
        'description': 'Date for this lead delivery data point',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
        'is_sortable': True,
    })

    # Metric type (delivered, accepted, rejected)
    metric_type = Column(String(20), info={
        'display_name': 'Metric Type',
        'description': 'Type of lead delivery metric',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
        'is_sortable': False,
    })

    # Count for this metric
    count = Column(Integer, info={
        'display_name': 'Count',
        'description': 'Number of leads for this metric type',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_filterable': True,
        'is_sortable': True,
    })

    # For seller-specific data (null for aggregated)
    id_seller = Column(Integer, nullable=True, info={
        'display_name': 'Seller ID',
        'description': 'Seller ID for seller-specific data (null for aggregated)',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_filterable': True,
        'is_sortable': False,
    })

    # Define field lists
    readable_fields = [
        'id', 'date', 'metric_type', 'count', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'date', 'metric_type', 'count', 'id_seller'
    ]

    searchable_fields = [
        'metric_type'
    ]
