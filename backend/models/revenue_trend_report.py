from sqlalchemy import Column, Integer, Float, Date
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class RevenueTrendReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'revenue_trend_reports'

    # The date for this data point
    date = Column(Date, info={
        'display_name': 'Date',
        'description': 'Date for this revenue data point',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
        'is_sortable': True,
    })

    # Revenue amount for this date
    revenue = Column(Float, info={
        'display_name': 'Revenue',
        'description': 'Revenue amount for this date',
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
        'id', 'date', 'revenue', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'date', 'revenue', 'id_seller'
    ]

    searchable_fields = [
        'date'
    ]
