from enum import Enum


class DatasetOrderStatus(Enum):
    """Overall lifecycle state for a dataset order."""

    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DISPUTED = 'disputed'
    REFUNDED = 'refunded'
    UNDER_REVIEW = 'under_review'
    COMPLETED = 'completed'
    EXPIRED = 'expired'


class DatasetLicenceStatus(Enum):
    """Licence activity status for purchased dataset orders."""

    ACTIVE = 'active'
    EXPIRING_SOON = 'expiring_soon'
    EXPIRING_TODAY = 'expiring_today'
    EXPIRED = 'expired'
    NOT_ISSUED = 'not_issued'


class DatasetForwardingStatus(Enum):
    """Forwarding attempt outcome for delivered dataset batches."""

    SUCCESS = 'success'
    FAIL = 'fail'
    PENDING = 'pending'
    NOT_APPLICABLE = 'not_applicable'


class DatasetDisputeStatus(Enum):
    """Resolution stage for dataset disputes."""

    NONE = 'none'
    AWAITING_REPLY = 'awaiting_reply'
    UNDER_REVIEW = 'under_review'
    RESOLVED = 'resolved'
    REFUNDED = 'refunded'


class DatasetRefundStatus(Enum):
    """Refund progress for dataset orders."""

    NONE = 'none'
    PENDING = 'pending'
    PARTIAL = 'partial'
    FULL = 'full'
    REJECTED = 'rejected'


class DatasetDeliveryStatus(Enum):
    """Outcome of an individual dataset delivery row."""

    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DISPUTED = 'disputed'
