from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin
from backend.models.dataset_order_enums import (
    DatasetDisputeStatus,
    DatasetForwardingStatus,
    DatasetLicenceStatus,
    DatasetOrderStatus,
    DatasetRefundStatus,
)


class DatasetOrder(CommonColumnsMixin, BaseModel):
    __tablename__ = 'dataset_orders'

    _info = {
        'description': 'Tracks dataset purchases and downstream operational status.',
        'type': 'transactional',
    }

    order_code: Mapped[str] = mc(
        String(30),
        unique=True,
        nullable=False,
        info={
            'name': 'order_code',
            'display_name': 'Order Code',
            'description': 'External reference for the dataset order (e.g. LLO825135).',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'max_length': 30,
        },
    )

    id_product: Mapped[int] = mc(
        ForeignKey('products.id', name='fk_dataset_orders_products'),
        nullable=False,
        info={
            'name': 'id_product',
            'display_name': 'Product',
            'description': 'FK to the purchased dataset product.',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    id_buyer_company: Mapped[int] = mc(
        ForeignKey('companies.id', name='fk_dataset_orders_buyer_company'),
        nullable=False,
        info={
            'name': 'id_buyer_company',
            'display_name': 'Buyer Company',
            'description': 'FK to the company purchasing the dataset order.',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    id_seller_company: Mapped[int] = mc(
        ForeignKey('companies.id', name='fk_dataset_orders_seller_company'),
        nullable=False,
        info={
            'name': 'id_seller_company',
            'display_name': 'Seller Company',
            'description': 'FK to the company fulfilling the dataset order.',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    ordered_on: Mapped[datetime] = mc(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
        info={
            'name': 'ordered_on',
            'display_name': 'Ordered On',
            'description': 'Timestamp when the dataset order was placed.',
            'display_type': 'datetime',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    quantity: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'quantity',
            'display_name': 'Quantity',
            'description': 'Total units or records purchased.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    unit_price: Mapped[float] = mc(
        Numeric(12, 2),
        nullable=False,
        info={
            'name': 'unit_price',
            'display_name': 'Unit Price',
            'description': 'Price per record at time of purchase.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    total_value: Mapped[float] = mc(
        Numeric(12, 2),
        nullable=False,
        info={
            'name': 'total_value',
            'display_name': 'Total Value',
            'description': 'Contract value (quantity × unit price).',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    currency: Mapped[str] = mc(
        String(3),
        default='GBP',
        nullable=False,
        info={
            'name': 'currency',
            'display_name': 'Currency',
            'description': 'ISO currency code for the order value.',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'max_length': 3,
        },
    )

    dupecheck_passed: Mapped[bool] = mc(
        Boolean,
        default=True,
        nullable=False,
        info={
            'name': 'dupecheck_passed',
            'display_name': 'DupeCheck Passed',
            'description': 'Indicates whether duplicate cleansing passed for this order.',
            'display_type': 'boolean',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    tps_match_count: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'tps_match_count',
            'display_name': 'TPS Match Count',
            'description': 'Number of records hitting TPS during validation.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    status: Mapped[str] = mc(
        String(20),
        default=DatasetOrderStatus.ACCEPTED.value,
        nullable=False,
        info={
            'name': 'status',
            'display_name': 'Order Status',
            'description': 'Lifecycle status for the dataset order.',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.replace('_', ' ').title()}
                    for status in DatasetOrderStatus
                ],
            },
        },
    )

    licence_status: Mapped[str] = mc(
        String(20),
        default=DatasetLicenceStatus.ACTIVE.value,
        nullable=False,
        info={
            'name': 'licence_status',
            'display_name': 'Licence Status',
            'description': 'Current licence status for the purchased dataset.',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.replace('_', ' ').title()}
                    for status in DatasetLicenceStatus
                ],
            },
        },
    )

    licence_expires_on: Mapped[date | None] = mc(
        Date,
        info={
            'name': 'licence_expires_on',
            'display_name': 'Licence Expires On',
            'description': 'Date when the dataset licence expires.',
            'display_type': 'date',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    dispute_status: Mapped[str] = mc(
        String(20),
        default=DatasetDisputeStatus.NONE.value,
        nullable=False,
        info={
            'name': 'dispute_status',
            'display_name': 'Dispute Status',
            'description': 'High-level dispute state for the order.',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.replace('_', ' ').title()}
                    for status in DatasetDisputeStatus
                ],
            },
        },
    )

    dispute_count: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'dispute_count',
            'display_name': 'Dispute Count',
            'description': 'Number of active disputes linked to this order.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    dispute_summary: Mapped[str | None] = mc(
        Text,
        info={
            'name': 'dispute_summary',
            'display_name': 'Dispute Summary',
            'description': 'Short text describing outstanding dispute reasons.',
            'display_type': 'textarea',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    refund_status: Mapped[str] = mc(
        String(20),
        default=DatasetRefundStatus.NONE.value,
        nullable=False,
        info={
            'name': 'refund_status',
            'display_name': 'Refund Status',
            'description': 'Refund progress for this order.',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.replace('_', ' ').title()}
                    for status in DatasetRefundStatus
                ],
            },
        },
    )

    refund_value: Mapped[float | None] = mc(
        Numeric(12, 2),
        info={
            'name': 'refund_value',
            'display_name': 'Refund Value',
            'description': 'Value refunded to date for this order.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    coverage_enabled: Mapped[bool] = mc(
        Boolean,
        default=True,
        nullable=False,
        info={
            'name': 'coverage_enabled',
            'display_name': 'Coverage',
            'description': 'Indicates if agreed coverage requirements were met.',
            'display_type': 'boolean',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    advanced_filters_enabled: Mapped[bool] = mc(
        Boolean,
        default=False,
        nullable=False,
        info={
            'name': 'advanced_filters_enabled',
            'display_name': 'Advanced Filters',
            'description': 'Whether custom filtering logic was applied for the order.',
            'display_type': 'boolean',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    query_count: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'query_count',
            'display_name': 'Query Count',
            'description': 'Total number of queries used to build the dataset.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    query_rules: Mapped[list[dict[str, str]] | None] = mc(
        JSONB,
        info={
            'name': 'query_rules',
            'display_name': 'Query Rules',
            'description': 'Structured filters executed to source the dataset.',
            'display_type': 'json_editor',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    forwarding_status: Mapped[str] = mc(
        String(20),
        default=DatasetForwardingStatus.SUCCESS.value,
        nullable=False,
        info={
            'name': 'forwarding_status',
            'display_name': 'Forwarding Status',
            'description': 'Overall forwarding outcome for the dataset delivery.',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.replace('_', ' ').title()}
                    for status in DatasetForwardingStatus
                ],
            },
        },
    )

    retry_count_total: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'retry_count_total',
            'display_name': 'Retry Count',
            'description': 'Aggregate retry attempts across deliveries.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 0,
        },
    )

    notes: Mapped[str | None] = mc(
        Text,
        info={
            'name': 'notes',
            'display_name': 'Internal Notes',
            'description': 'Operational notes for CS / compliance teams.',
            'display_type': 'textarea',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    updateable_fields = [
        'order_code',
        'id_product',
        'id_buyer_company',
        'id_seller_company',
        'ordered_on',
        'quantity',
        'unit_price',
        'total_value',
        'currency',
        'dupecheck_passed',
        'tps_match_count',
        'status',
        'licence_status',
        'licence_expires_on',
        'dispute_status',
        'dispute_count',
        'dispute_summary',
        'refund_status',
        'refund_value',
        'coverage_enabled',
        'advanced_filters_enabled',
        'query_count',
        'query_rules',
        'forwarding_status',
        'retry_count_total',
        'notes',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'order_code',
        'id_product',
        'id_buyer_company',
        'id_seller_company',
        'ordered_on',
        'quantity',
        'unit_price',
        'total_value',
        'currency',
        'dupecheck_passed',
        'tps_match_count',
        'status',
        'licence_status',
        'licence_expires_on',
        'dispute_status',
        'dispute_count',
        'dispute_summary',
        'refund_status',
        'refund_value',
        'coverage_enabled',
        'advanced_filters_enabled',
        'query_count',
        'query_rules',
        'forwarding_status',
        'retry_count_total',
        'notes',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'order_code',
        'ordered_on',
        'quantity',
        'unit_price',
        'total_value',
        'tps_match_count',
        'status',
        'licence_status',
        'licence_expires_on',
        'dispute_count',
        'refund_value',
        'forwarding_status',
        'retry_count_total',
    ]

    searchable_fields = [
        'order_code',
        'dispute_summary',
        'notes',
    ]

    filterable_fields = [
        'id',
        'order_code',
        'id_product',
        'id_buyer_company',
        'id_seller_company',
        'ordered_on',
        'status',
        'licence_status',
        'dispute_status',
        'refund_status',
        'coverage_enabled',
        'advanced_filters_enabled',
        'forwarding_status',
    ]
