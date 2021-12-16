from collections import Callable
from functools import wraps
from src.libs.custom_exceptions.redis_exceptions import  ClosedPubSubException


def needs_open_connection(validated_function: Callable):
    """Decorator for functions where an opened pubsub is required. Checks if the self.closed: bool instance attribute
    is True, if not, raises a "ClosedPubSubException exception

    This function should decorate instance methods where a pubsub operation that requires an opened connection is
    needed, like subscribing and unsubscribing to channels"""

    @wraps(validated_function)
    def check_connection(self, *args, **kwargs):
        if self.closed:
            raise ClosedPubSubException("ERROR: Cant perform operation on closed pubsub.")

        return validated_function(self, *args, **kwargs)

    return check_connection
