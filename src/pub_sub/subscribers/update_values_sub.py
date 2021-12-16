import inspect
import json
from functools import wraps
from typing import Callable, Any, Dict
from src.libs.custom_exceptions.fetching_exception import MethodNotCompatibleError
from src.libs.redis_cache.redis_pub_sub import RedisSub


def subscription_builder(channel: str, handler: Callable[[Any], None]) -> RedisSub:
    """Subscribes a function to a specified channel
    in the pubsub manager, returns the subscription object representing said subscription."""

    redis_sub = RedisSub()
    redis_sub.subscribe(channel, handler)
    return redis_sub


def subscribe_to_update_request(handler: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for subscribing a function to the
    'update-dolarblue-values' channel when said function is called.

    The function to decorate can have any arguments or kwargs."""

    @wraps(handler)
    def provider(*args: Any, **kwargs: Any) -> None:
        def update_request_handler(_: Any) -> Any:

            handler(*args, **kwargs)

        subscription_builder("update-dolarblue-values", update_request_handler)

    return provider


def subscribe_to_cache_updated(handler: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for subscribing a function to the
    'dolarblue-values-updated' channel when said function is called.

    It provides a report to the decorated function, so it MUST accept 'report:Dict[str, bool]'
    as a kwarg"""

    # Check method compatibility DEPRECATED in python 3.10, not needed anymore
    inspected_handler = inspect.getfullargspec(handler)

    handler_has_report = "report" in inspected_handler.args
    report_is_dict = Dict[str,
                          bool] == inspected_handler.annotations.get("report")

    if (handler_has_report and report_is_dict) is not True:
        raise MethodNotCompatibleError("Decorated function is incompatible:\
        it has no 'report: Dict[str, bool]' argument")

    @wraps(handler)
    def provider(*args: Any, **kwargs: Any) -> None:
        def values_updated_handler(message: Dict[str, Any]) -> None:

            # Provide the report to the handler
            report_data: dict[str, bool] = json.loads(message["data"])
            kwargs["report"] = report_data

            handler(*args, **kwargs)

        subscription_builder("dolarblue-values-updated",
                             values_updated_handler)

    return provider
