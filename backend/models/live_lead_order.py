from datetime import date, datetime, time

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.live_lead_enums import (
    LiveLeadConnectionStatus,
    LiveLeadDeliveryDay,
    LiveLeadDeliveryStatus,
    LiveLeadOrderStatus,
)
from backend.models.mixins import CommonColumnsMixin


class LiveLeadOrder(CommonColumnsMixin, BaseModel):
    __tablename__ = 'live_lead_orders'

    _info = {
        'description': 'Tracks live lead purchase agreements, delivery progress, and API connectivity.',
        'type': 'transactional',
        'api': {
            'is_enabled': True,
            'class_name': 'LiveLeadOrder',
            'name': 'Live Lead Order',
            'singular': 'live_lead_order',
            'plural': 'live_lead_orders',
            'routes': ['get_one', 'get_all', 'post', 'patch', 'delete'],
            'route_class': 'LiveLeadOrderRoutes',
            'action_class': 'LiveLeadOrderActions',
        },
    }

    order_code: Mapped[str] = mc(
        String(50),
        unique=True,
        nullable=False,
        info={
            'name': 'order_code',
            'display_name': 'Order Code',
            'description': 'Unique code identifying the live lead order',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    product_id: Mapped[int] = mc(
        ForeignKey('products.id', name='fk_live_lead_orders_products'),
        nullable=False,
        info={
            'name': 'product_id',
            'display_name': 'Product',
            'description': 'FK to product (lead vertical)',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    buyer_id: Mapped[int] = mc(
        ForeignKey('users.id', name='fk_live_lead_orders_buyer'),
        nullable=False,
        info={
            'name': 'buyer_id',
            'display_name': 'Buyer',
            'description': 'FK to user purchasing live leads',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    seller_id: Mapped[int] = mc(
        ForeignKey('users.id', name='fk_live_lead_orders_seller'),
        nullable=False,
        info={
            'name': 'seller_id',
            'display_name': 'Seller',
            'description': 'FK to user providing live leads',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    ordered_on: Mapped[date] = mc(
        Date,
        nullable=False,
        info={
            'name': 'ordered_on',
            'display_name': 'Ordered On',
            'description': 'Date the live lead order was placed',
            'display_type': 'date',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    leads_ordered: Mapped[int] = mc(
        Integer,
        nullable=False,
        info={
            'name': 'leads_ordered',
            'display_name': 'Leads Ordered',
            'description': 'Total number of live leads purchased',
            'display_type': 'number',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': False,
            'is_sortable': True,
            'is_filterable': True,
            'min_value': 1,
        },
    )

    leads_delivered: Mapped[int] = mc(
        Integer,
        default=0,
        nullable=False,
        info={
            'name': 'leads_delivered',
            'display_name': 'Leads Delivered',
            'description': 'Count of leads successfully delivered',
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

    connection_status: Mapped[str] = mc(
        String(40),
        default=LiveLeadConnectionStatus.NO_CONNECTIONS.value,
        info={
            'name': 'connection_status',
            'display_name': 'Connection Status',
            'description': 'Connectivity state between buyer and seller systems',
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
                    for status in LiveLeadConnectionStatus
                ],
            },
        },
    )

    criteria: Mapped[str | None] = mc(
        Text,
        info={
            'name': 'criteria',
            'display_name': 'Lead Criteria',
            'description': 'Optional filtering conditions for lead delivery',
            'display_type': 'textarea',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    api_endpoint_url: Mapped[str | None] = mc(
        String(500),
        info={
            'name': 'api_endpoint_url',
            'display_name': 'API Endpoint URL',
            'description': 'Buyer ingestion endpoint for live lead delivery',
            'display_type': 'text',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    api_auth_key: Mapped[str | None] = mc(
        String(255),
        info={
            'name': 'api_auth_key',
            'display_name': 'API Auth Key',
            'description': 'Credential used to authenticate to buyer endpoint',
            'display_type': 'password',
            'is_visible': False,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    api_fields: Mapped[list[str] | None] = mc(
        ARRAY(String(100)),
        info={
            'name': 'api_fields',
            'display_name': 'API Fields',
            'description': 'Field mapping expected by the buyer API',
            'display_type': 'json_editor',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': False,
            'is_sortable': False,
            'is_filterable': False,
        },
    )

    api_is_connected: Mapped[bool] = mc(
        Boolean,
        default=False,
        nullable=False,
        info={
            'name': 'api_is_connected',
            'display_name': 'API Connected',
            'description': 'Indicates whether API credentials are validated',
            'display_type': 'boolean',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    api_last_checked_at: Mapped[datetime | None] = mc(
        DateTime(timezone=True),
        info={
            'name': 'api_last_checked_at',
            'display_name': 'API Last Checked At',
            'description': 'Timestamp of last connection validation',
            'display_type': 'datetime',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    status: Mapped[str] = mc(
        String(40),
        default=LiveLeadOrderStatus.AWAITING_START_DATE.value,
        info={
            'name': 'status',
            'display_name': 'Order Status',
            'description': 'Lifecycle status of the live lead order',
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
                    for status in LiveLeadOrderStatus
                ],
            },
        },
    )

    start_date: Mapped[date | None] = mc(
        Date,
        info={
            'name': 'start_date',
            'display_name': 'Start Date',
            'description': 'Date when delivery should begin',
            'display_type': 'date',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    end_date: Mapped[date | None] = mc(
        Date,
        info={
            'name': 'end_date',
            'display_name': 'End Date',
            'description': 'Date when delivery should end',
            'display_type': 'date',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'order_code',
        'product_id',
        'buyer_id',
        'seller_id',
        'ordered_on',
        'leads_ordered',
        'leads_delivered',
        'connection_status',
        'criteria',
        'api_endpoint_url',
        'api_auth_key',
        'api_fields',
        'api_is_connected',
        'api_last_checked_at',
        'status',
        'start_date',
        'end_date',
    ]

    readable_fields = [
        'id',
        'order_code',
        'product_id',
        'buyer_id',
        'seller_id',
        'ordered_on',
        'leads_ordered',
        'leads_delivered',
        'progress_percent',
        'connection_status',
        'criteria',
        'api_endpoint_url',
        'api_is_connected',
        'api_last_checked_at',
        'status',
        'start_date',
        'end_date',
        'created_at',
        'last_updated_at',
    ]

    sortable_fields = [
        'id',
        'order_code',
        'ordered_on',
        'leads_ordered',
        'leads_delivered',
        'status',
        'created_at',
    ]

    searchable_fields = [
        'order_code',
        'criteria',
    ]

    filterable_fields = [
        'id',
        'product_id',
        'buyer_id',
        'seller_id',
        'ordered_on',
        'status',
        'connection_status',
        'api_is_connected',
        'start_date',
        'end_date',
    ]

    @property
    def progress_percent(self) -> float:
        if not self.leads_ordered:
            return 0.0
        return round((self.leads_delivered / self.leads_ordered) * 100, 2)


class LiveLeadDeliverySchedule(CommonColumnsMixin, BaseModel):
    __tablename__ = 'delivery_schedules'
    __table_args__ = (
        UniqueConstraint('order_id', 'day_of_week', name='uq_delivery_schedule_order_day'),
        {
            'info': {
                'token': 'live_lead_delivery_schedule',
                'name': 'Live Lead Delivery Schedule',
                'description': 'Recurring delivery slots for a live lead order',
                'type': 'normal',
                'can_login': False,
                'api': {
                    'is_enabled': True,
                    'class_name': 'LiveLeadDeliverySchedule',
                    'name': 'Live Lead Delivery Schedule',
                    'singular': 'live_lead_delivery_schedule',
                    'plural': 'live_lead_delivery_schedules',
                    'routes': ['get_one', 'get_all', 'post', 'patch', 'delete'],
                    'route_class': 'LiveLeadDeliveryScheduleRoutes',
                    'action_class': 'LiveLeadDeliveryScheduleActions',
                },
            }
        },
    )

    updateable_fields = [
        'order_id',
        'day_of_week',
        'start_time',
        'end_time',
        'capacity',
    ]

    readable_fields = [
        'id',
        'order_id',
        'day_of_week',
        'start_time',
        'end_time',
        'capacity',
        'created_at',
        'last_updated_at',
    ]

    sortable_fields = [
        'id',
        'order_id',
        'day_of_week',
        'start_time',
        'end_time',
        'capacity',
    ]

    searchable_fields = [
        'day_of_week',
    ]

    filterable_fields = [
        'order_id',
        'day_of_week',
    ]

    order_id: Mapped[int] = mc(
        ForeignKey('live_lead_orders.id', name='fk_delivery_schedules_order'),
        nullable=False,
        info={
            'name': 'order_id',
            'display_name': 'Live Lead Order',
            'description': 'FK to live lead order',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    day_of_week: Mapped[str] = mc(
        String(10),
        nullable=False,
        info={
            'name': 'day_of_week',
            'display_name': 'Day of Week',
            'description': 'Day of the week for delivery slot',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': day.value, 'label': day.name.title()}
                    for day in LiveLeadDeliveryDay
                ],
            },
        },
    )

    start_time: Mapped[time | None] = mc(
        Time(timezone=False),
        info={
            'name': 'start_time',
            'display_name': 'Start Time',
            'description': 'Start time for delivery window',
            'display_type': 'time',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    end_time: Mapped[time | None] = mc(
        Time(timezone=False),
        info={
            'name': 'end_time',
            'display_name': 'End Time',
            'description': 'End time for delivery window',
            'display_type': 'time',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    capacity: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'capacity',
            'display_name': 'Capacity',
            'description': 'Maximum number of leads deliverable in the window',
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


class LiveLeadOrderStatusHistory(CommonColumnsMixin, BaseModel):
    __tablename__ = 'order_status_history'

    _info = {
        'description': 'Historical log of status transitions for live lead orders.',
        'type': 'normal',
        'api': {
            'is_enabled': True,
            'class_name': 'LiveLeadOrderStatusHistory',
            'name': 'Live Lead Order Status History',
            'singular': 'live_lead_order_status_history',
            'plural': 'live_lead_order_status_histories',
            'routes': ['get_one', 'get_all', 'post', 'patch', 'delete'],
            'route_class': 'LiveLeadOrderStatusHistoryRoutes',
            'action_class': 'LiveLeadOrderStatusHistoryActions',
        },
    }

    order_id: Mapped[int] = mc(
        ForeignKey('live_lead_orders.id', name='fk_order_status_history_order'),
        nullable=False,
        info={
            'name': 'order_id',
            'display_name': 'Live Lead Order',
            'description': 'FK to live lead order',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'order_id',
        'status',
        'changed_at',
        'changed_by',
        'remarks',
    ]

    readable_fields = [
        'id',
        'order_id',
        'status',
        'changed_at',
        'changed_by',
        'remarks',
        'created_at',
        'last_updated_at',
    ]

    sortable_fields = [
        'id',
        'order_id',
        'status',
        'changed_at',
        'created_at',
    ]

    searchable_fields = [
        'remarks',
    ]

    filterable_fields = [
        'order_id',
        'status',
        'changed_by',
        'changed_at',
    ]

    status: Mapped[str] = mc(
        String(40),
        nullable=False,
        info={
            'name': 'status',
            'display_name': 'Status',
            'description': 'Status applied to the order',
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
                    for status in LiveLeadOrderStatus
                ],
            },
        },
    )

    changed_at: Mapped[datetime] = mc(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
        info={
            'name': 'changed_at',
            'display_name': 'Changed At',
            'description': 'Timestamp of the status change',
            'display_type': 'datetime',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    changed_by: Mapped[int | None] = mc(
        ForeignKey('users.id', name='fk_order_status_history_user'),
        info={
            'name': 'changed_by',
            'display_name': 'Changed By',
            'description': 'User responsible for the status change',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    remarks: Mapped[str | None] = mc(
        Text,
        info={
            'name': 'remarks',
            'display_name': 'Remarks',
            'description': 'Additional context about the status change',
            'display_type': 'textarea',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': False,
            'is_filterable': False,
        },
    )


class DailyLeadDeliveryLog(CommonColumnsMixin, BaseModel):
    __tablename__ = 'daily_lead_delivery_log'

    _info = {
        'description': 'Daily snapshot of live lead delivery performance.',
        'type': 'normal',
        'api': {
            'is_enabled': True,
            'class_name': 'DailyLeadDeliveryLog',
            'name': 'Daily Lead Delivery Log',
            'singular': 'daily_lead_delivery_log',
            'plural': 'daily_lead_delivery_logs',
            'routes': ['get_one', 'get_all', 'post', 'patch', 'delete'],
            'route_class': 'DailyLeadDeliveryLogRoutes',
            'action_class': 'DailyLeadDeliveryLogActions',
        },
    }

    order_id: Mapped[int] = mc(
        ForeignKey('live_lead_orders.id', name='fk_daily_lead_delivery_log_order'),
        nullable=False,
        info={
            'name': 'order_id',
            'display_name': 'Live Lead Order',
            'description': 'FK to live lead order',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'order_id',
        'date',
        'leads_sent',
        'success_count',
        'failure_count',
        'delivery_status',
    ]

    readable_fields = [
        'id',
        'order_id',
        'date',
        'leads_sent',
        'success_count',
        'failure_count',
        'delivery_status',
        'created_at',
        'last_updated_at',
    ]

    sortable_fields = [
        'id',
        'order_id',
        'date',
        'leads_sent',
        'success_count',
        'failure_count',
        'delivery_status',
    ]

    searchable_fields = []

    filterable_fields = [
        'order_id',
        'date',
        'delivery_status',
    ]

    date: Mapped[date] = mc(
        Date,
        nullable=False,
        info={
            'name': 'date',
            'display_name': 'Delivery Date',
            'description': 'Date the delivery summary covers',
            'display_type': 'date',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    leads_sent: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'leads_sent',
            'display_name': 'Leads Sent',
            'description': 'Total leads attempted for delivery',
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

    success_count: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'success_count',
            'display_name': 'Successful Deliveries',
            'description': 'Number of leads accepted by buyer API',
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

    failure_count: Mapped[int | None] = mc(
        Integer,
        info={
            'name': 'failure_count',
            'display_name': 'Failed Deliveries',
            'description': 'Number of leads rejected by buyer API',
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

    delivery_status: Mapped[str | None] = mc(
        String(20),
        info={
            'name': 'delivery_status',
            'display_name': 'Delivery Status',
            'description': 'Overall delivery outcome for the day',
            'display_type': 'select',
            'is_visible': True,
            'is_editable': True,
            'is_required': False,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
            'display_settings': {
                'options': [
                    {'value': status.value, 'label': status.name.title()}
                    for status in LiveLeadDeliveryStatus
                ],
            },
        },
    )
