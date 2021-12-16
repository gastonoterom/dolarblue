from functools import wraps
from typing import Any, Callable
from src.libs.custom_exceptions.redis_exceptions import ClosedPubSubException


def needs_open_connection(validated_function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for functions where an opened pubsub is required.
    Checks if the self.closed: bool instance attribute is True, if not, raises a
    "ClosedPubSubException exception

    This function should decorate instance methods where a pubsub operation that
    requires an opened connection is needed, like subscribing and unsubscribing to channels.
    This function is for instance methods of a RedisSub class, or any other class that matches
    its protocol (not yet implemented)"""

    @ wraps(validated_function)
    def check_connection(self, *args: Any, **kwargs: Any) -> Any:
        if self.closed:
            raise ClosedPubSubException(
                "ERROR: Cant perform operation on closed pubsub.")

        return validated_function(self, *args, **kwargs)

    return check_connection
