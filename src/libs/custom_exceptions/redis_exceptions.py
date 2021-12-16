

class SubscriptionNotFoundException(Exception):
    """Raised when trying to unsubscribe from a never subscribed channel"""


class ClosedPubSubException(Exception):
    """Raised when trying to unsubscribe from a never subscribed channel"""
