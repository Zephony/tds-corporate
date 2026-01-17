from sqlalchemy import Column, Integer, String
from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class TopDisputeReasonsReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'top_dispute_reasons_reports'

    # Dispute reason in snake_case
    reason = Column(String(100), info={
        'display_name': 'Reason',
        'description': 'Dispute reason category',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_filterable': True,
    })

    # Number of purchases/disputes for this reason
    purchase_count = Column(Integer, info={
        'display_name': 'Purchase Count',
        'description': 'Number of purchases/disputes for this reason',
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
        'id', 'reason', 'purchase_count', 'id_seller',
        'created_at', 'last_updated_at'
    ]

    updateable_fields = [
        'reason', 'purchase_count', 'id_seller'
    ]

    searchable_fields = [
        'reason'
    ]
