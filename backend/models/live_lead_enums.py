from enum import Enum


class LiveLeadConnectionStatus(Enum):
    """Represents the connection state between buyer and seller systems."""

    NO_CONNECTIONS = 'no_connections'
    BUYER_NOT_CONNECTED = 'buyer_not_connected'
    BUYER_SELLER_CONNECTED = 'buyer_seller_connected'


class LiveLeadOrderStatus(Enum):
    """Lifecycle states for a live lead order."""

    AWAITING_START_DATE = 'awaiting_start_date'
    API_NOT_CONNECTED = 'api_not_connected'
    START_DATE_NOT_SET = 'start_date_not_set'
    AWAITING_START = 'awaiting_start'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    REFUNDED = 'refunded'
    EXPIRED = 'expired'
    DISPUTED = 'disputed'
    CHARGEBACK = 'chargeback'


class LiveLeadDeliveryStatus(Enum):
    """Daily delivery summary outcomes."""

    COMPLETED = 'completed'
    PARTIAL = 'partial'
    FAILED = 'failed'


class LiveLeadDeliveryDay(Enum):
    """Days of the week for delivery schedules."""

    SUNDAY = 'sunday'
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
