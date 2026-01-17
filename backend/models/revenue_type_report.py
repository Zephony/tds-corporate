from sqlalchemy import Column, Integer, String, Float
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class RevenueTypeReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'revenue_type_reports'

    # Type of revenue (TDS, Ad Portal, DD, etc.)
    revenue_type = Column(String(50), info={
        'display_name': 'Revenue Type',
        'description': 'Type of revenue source',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
    })

    # Revenue amount for this type
    revenue_amount = Column(Float, info={
        'display_name': 'Revenue Amount',
        'description': 'Revenue amount for this type',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_filterable': True,
        'is_sortable': True,
    })

    # Percentage of total revenue
    percentage = Column(Float, info={
        'display_name': 'Percentage',
        'description': 'Percentage of total revenue',
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
        'id', 'revenue_type', 'revenue_amount', 'percentage', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'revenue_type', 'revenue_amount', 'percentage', 'id_seller'
    ]

    searchable_fields = [
        'revenue_type'
    ]
