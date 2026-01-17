from sqlalchemy import Column, String, Integer
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class TopCategoriesByPurchaseReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'top_categories_by_purchase_reports'

    # Category name in snake_case
    category = Column(String(100), info={
        'display_name': 'Category',
        'description': 'Product category name',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
        'is_sortable': False,
    })

    # Purchase count for this category
    purchase_count = Column(Integer, info={
        'display_name': 'Purchase Count',
        'description': 'Number of purchases for this category',
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
        'id', 'category', 'purchase_count', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'category', 'purchase_count', 'id_seller'
    ]

    searchable_fields = [
        'category'
    ]
