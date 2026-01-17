from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin
from backend.models.dataset_order_enums import (
    DatasetDeliveryStatus,
    DatasetForwardingStatus,
)


class DatasetOrderDelivery(CommonColumnsMixin, BaseModel):
    __tablename__ = 'dataset_order_deliveries'

    _info = {
        'description': 'Individual delivery attempts for dataset orders.',
        'type': 'transactional',
        'api': {
            'is_enabled': False,
        },
    }

    id_dataset_order: Mapped[int] = mc(
        ForeignKey('dataset_orders.id', name='fk_dataset_order_deliveries_dataset_order'),
        nullable=False,
        info={
            'name': 'id_dataset_order',
            'display_name': 'Dataset Order',
            'description': 'FK to the parent dataset order.',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    delivery_code: Mapped[str] = mc(
        String(30),
        unique=True,
        nullable=False,
        info={
            'name': 'delivery_code',
            'display_name': 'Delivery Code',
            'description': 'Reference for a delivery batch (e.g. TMP8259102).',
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

    delivered_on: Mapped[datetime] = mc(
        DateTime(timezone=True),
        nullable=False,
        info={
            'name': 'delivered_on',
            'display_name': 'Delivered On',
            'description': 'Timestamp when the delivery was completed.',
            'display_type': 'datetime',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    hlr_result: Mapped[str] = mc(
        String(10),
        default='yes',
        nullable=False,
        info={
            'name': 'hlr_result',
            'display_name': 'HLR',
            'description': 'HLR verification outcome for the delivery (Yes/No/N/A).',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': 'yes', 'label': 'Yes'},
                    {'value': 'no', 'label': 'No'},
                    {'value': 'n/a', 'label': 'N/A'},
                ],
            },
        },
    )

    llv_result: Mapped[str] = mc(
        String(10),
        default='yes',
        nullable=False,
        info={
            'name': 'llv_result',
            'display_name': 'LLV',
            'description': 'LLV verification outcome for the delivery (Yes/No/N/A).',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': 'yes', 'label': 'Yes'},
                    {'value': 'no', 'label': 'No'},
                    {'value': 'n/a', 'label': 'N/A'},
                ],
            },
        },
    )

    criteria_met: Mapped[bool] = mc(
        Boolean,
        default=True,
        nullable=False,
        info={
            'name': 'criteria_met',
            'display_name': 'Criteria',
            'description': 'Whether delivery met agreed criteria.',
            'display_type': 'boolean',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    status: Mapped[str] = mc(
        String(20),
        default=DatasetDeliveryStatus.ACCEPTED.value,
        nullable=False,
        info={
            'name': 'status',
            'display_name': 'Status',
            'description': 'Delivery status for this batch.',
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
                    for status in DatasetDeliveryStatus
                ],
            },
        },
    )

    retry_count: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'retry_count',
            'display_name': 'Retry Count',
            'description': 'Number of retries attempted for this delivery.',
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

    dispute_reason: Mapped[str | None] = mc(
        String(255),
        info={
            'name': 'dispute_reason',
            'display_name': 'Dispute Reason',
            'description': 'Reason provided when the delivery is disputed.',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'max_length': 255,
        },
    )

    api_code: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'api_code',
            'display_name': 'API Code',
            'description': 'Response code from forwarding attempt.',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    forwarding_status: Mapped[str] = mc(
        String(20),
        default=DatasetForwardingStatus.SUCCESS.value,
        nullable=False,
        info={
            'name': 'forwarding_status',
            'display_name': 'Forwarding',
            'description': 'Forwarding outcome for this delivery.',
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

    forwarding_notes: Mapped[str | None] = mc(
        Text,
        info={
            'name': 'forwarding_notes',
            'display_name': 'Forwarding Notes',
            'description': 'Additional notes captured during forwarding.',
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
        'id_dataset_order',
        'delivery_code',
        'delivered_on',
        'hlr_result',
        'llv_result',
        'criteria_met',
        'status',
        'retry_count',
        'dispute_reason',
        'api_code',
        'forwarding_status',
        'forwarding_notes',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'id_dataset_order',
        'delivery_code',
        'delivered_on',
        'hlr_result',
        'llv_result',
        'criteria_met',
        'status',
        'retry_count',
        'dispute_reason',
        'api_code',
        'forwarding_status',
        'forwarding_notes',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'delivery_code',
        'delivered_on',
        'retry_count',
        'api_code',
        'forwarding_status',
    ]

    searchable_fields = [
        'delivery_code',
        'dispute_reason',
        'forwarding_notes',
    ]

    filterable_fields = [
        'id',
        'id_dataset_order',
        'delivery_code',
        'delivered_on',
        'hlr_result',
        'llv_result',
        'criteria_met',
        'status',
        'forwarding_status',
    ]
