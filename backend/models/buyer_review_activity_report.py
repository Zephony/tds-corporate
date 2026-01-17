from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Integer, Numeric, DateTime, Date
from datetime import datetime, date

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class BuyerReviewActivityReport(CommonColumnsMixin, BaseModel):
    __tablename__ = 'buyer_review_activity_reports'

    _info = {
        'description': 'Buyer review activity reporting data for analytics',
        'type': 'report',
        'api': {
            'routes': [
                'get_all',
            ],
        },
    }

    # Buyer identification
    id_buyer: Mapped[int] = mc(Integer, nullable=False, info={
        'name': 'id_buyer',
        'display_name': 'Buyer ID',
        'description': 'Foreign key reference to the buyer user',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    user_name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'user_name',
        'display_name': 'User Name',
        'description': 'Display name of the buyer',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    user_email: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'user_email',
        'display_name': 'User Email',
        'description': 'Email address of the buyer',
        'display_type': 'email',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    signed_up_date: Mapped[datetime] = mc(DateTime(timezone=True), nullable=False, info={
        'name': 'signed_up_date',
        'display_name': 'Signed Up Date',
        'description': 'Date when the buyer signed up',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Review activity metrics
    reviews_left: Mapped[int] = mc(Integer, default=0, info={
        'name': 'reviews_left',
        'display_name': 'Reviews Left',
        'description': 'Total number of reviews written by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    avg_rating_given: Mapped[Numeric] = mc(Numeric(3, 1), default=0.0, info={
        'name': 'avg_rating_given',
        'display_name': 'Avg Rating Given',
        'description': 'Average star rating given by the buyer (e.g., 4.5)',
        'display_type': 'rating',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    negative_reviews: Mapped[int] = mc(Integer, default=0, info={
        'name': 'negative_reviews',
        'display_name': 'Negative Reviews',
        'description': 'Count of negative reviews given by the buyer',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    last_review_date: Mapped[date|None] = mc(Date, info={
        'name': 'last_review_date',
        'display_name': 'Last Review',
        'description': 'Date when the buyer left their most recent review',
        'display_type': 'date',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Status and metadata
    status: Mapped[str] = mc(String(50), default='ACTIVE_STATUS', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Current status of the buyer',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'reviews_left',
        'avg_rating_given',
        'negative_reviews',
        'last_review_date',
        'status',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'reviews_left',
        'avg_rating_given',
        'negative_reviews',
        'last_review_date',
        'status',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'reviews_left',
        'avg_rating_given',
        'negative_reviews',
        'last_review_date',
        'status',
    ]

    searchable_fields = [
        'id_buyer',
        'user_name',
        'user_email',
    ]

    filterable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_buyer',
        'user_name',
        'user_email',
        'signed_up_date',
        'reviews_left',
        'avg_rating_given',
        'negative_reviews',
        'last_review_date',
        'status',
    ]
