from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, Numeric, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Review(CommonColumnsMixin, BaseModel):
    __tablename__ = 'reviews'

    # Review content
    title: Mapped[str|None] = mc(String(255), info={
        'name': 'title',
        'display_name': 'Review Title',
        'description': 'Optional title for the review',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    
    review_text: Mapped[str] = mc(Text, nullable=False, info={
        'name': 'review_text',
        'display_name': 'Review Text',
        'description': 'Main content of the review',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    review_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'review_date',
        'display_name': 'Review Date',
        'description': 'Date and time when the review was submitted',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Recommendation flag
    is_recommended: Mapped[bool] = mc(Boolean, default=True, info={
        'name': 'is_recommended',
        'display_name': 'Recommended',
        'description': 'Whether the reviewer recommends this product',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Multi-category rating system (0.0 - 5.0 scale)
    accuracy_rating: Mapped[float|None] = mc(Numeric(3, 2), info={
        'name': 'accuracy_rating',
        'display_name': 'Accuracy Rating',
        'description': 'Rating for data accuracy (0.0 - 5.0)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0.0,
        'max_value': 5.0,
    })
    
    receptivity_rating: Mapped[float|None] = mc(Numeric(3, 2), info={
        'name': 'receptivity_rating',
        'display_name': 'Receptivity Rating',
        'description': 'Rating for receptivity (0.0 - 5.0)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0.0,
        'max_value': 5.0,
    })
    
    contact_rate_rating: Mapped[float|None] = mc(Numeric(3, 2), info={
        'name': 'contact_rate_rating',
        'display_name': 'Contact Rate Rating',
        'description': 'Rating for contact rate (0.0 - 5.0)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0.0,
        'max_value': 5.0,
    })
    
    overall_rating: Mapped[float] = mc(Numeric(3, 2), nullable=False, info={
        'name': 'overall_rating',
        'display_name': 'Overall Rating',
        'description': 'Overall rating (0.0 - 5.0)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0.0,
        'max_value': 5.0,
    })
    
    # Moderation and reporting
    reported_count: Mapped[int] = mc(Integer, default=0, info={
        'name': 'reported_count',
        'display_name': 'Reported Count',
        'description': 'Number of times this review was reported',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Should be updated programmatically
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    is_flagged: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'is_flagged',
        'display_name': 'Flagged for Review',
        'description': 'Whether this review is flagged for moderation',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    contains_offensive_words: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'contains_offensive_words',
        'display_name': 'Contains Offensive Words',
        'description': 'Whether offensive words were detected in this review',
        'display_type': 'checkbox',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    moderation_notes: Mapped[str|None] = mc(Text, info={
        'name': 'moderation_notes',
        'display_name': 'Moderation Notes',
        'description': 'Admin notes for review moderation',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Review status
    status: Mapped[str] = mc(String(20), default='PENDING', info={
        'name': 'status',
        'display_name': 'Review Status',
        'description': 'Current status of the review',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'ACTIVE', 'label': 'Active'},
                {'value': 'REJECTED', 'label': 'Rejected'},
                {'value': 'HIDDEN', 'label': 'Hidden'},
                {'value': 'FLAGGED', 'label': 'Flagged'}
            ]
        },
    })
    
    # Relationships (following id_* convention)
    id_product: Mapped[int] = mc(
        ForeignKey('products.id', name='fk_reviews_products'),
        nullable=False,
        info={
        'name': 'id_product',
        'display_name': 'Product',
        'description': 'FK to Product being reviewed',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_reviewer_user: Mapped[int] = mc(
        ForeignKey('users.id', name='fk_reviews_reviewer_user'),
        nullable=False,
        info={
        'name': 'id_reviewer_user',
        'display_name': 'Reviewer User',
        'description': 'FK to User who wrote the review',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_reviewer_company: Mapped[int] = mc(
        ForeignKey('companies.id', name='fk_reviews_reviewer_company'),
        nullable=False,
        info={
        'name': 'id_reviewer_company',
        'display_name': 'Reviewer Company',
        'description': 'FK to Company of the reviewer',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    id_order: Mapped[int|None] = mc(
        ForeignKey('orders.id', name='fk_reviews_orders'),
        info={
        'name': 'id_order',
        'display_name': 'Related Order',
        'description': 'FK to Order this review relates to (optional)',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'title',
        'review_text',
        'review_date',
        'is_recommended',
        'accuracy_rating',
        'receptivity_rating',
        'contact_rate_rating',
        'overall_rating',
        'is_flagged',
        'contains_offensive_words',
        'moderation_notes',
        'status',
        'id_product',
        'id_reviewer_user',
        'id_reviewer_company',
        'id_order',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'title',
        'review_text',
        'review_date',
        'is_recommended',
        'accuracy_rating',
        'receptivity_rating',
        'contact_rate_rating',
        'overall_rating',
        'reported_count',
        'is_flagged',
        'contains_offensive_words',
        'moderation_notes',
        'status',
        'id_product',
        'id_reviewer_user',
        'id_reviewer_company',
        'id_order',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'review_date',
        'is_recommended',
        'accuracy_rating',
        'receptivity_rating',
        'contact_rate_rating',
        'overall_rating',
        'reported_count',
        'is_flagged',
        'contains_offensive_words',
        'status',
    ]

    searchable_fields = [
        'title',
        'review_text',
        'moderation_notes',
    ]

    filterable_fields = [
        'id',
        'review_date',
        'is_recommended',
        'accuracy_rating',
        'receptivity_rating',
        'contact_rate_rating',
        'overall_rating',
        'reported_count',
        'is_flagged',
        'contains_offensive_words',
        'status',
        'id_product',
        'id_reviewer_user',
        'id_reviewer_company',
        'id_order',
    ]
