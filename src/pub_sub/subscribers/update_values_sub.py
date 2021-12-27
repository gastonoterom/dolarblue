from datetime import datetime
import json
from functools import wraps
import logging
from typing import Callable, Any, Dict, Optional
from src.classes.dolar_blue import DolarBlue, DolarBlueSource
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


def parse_json_report(json_payload: str) -> Dict[str, Optional[DolarBlue]]:
    """This function parses a JSON string containing each source and it's dolarblue value
    to return a dictionary with a python object representing the dolarblue."""
    report_data = json.loads(json_payload)
    parsed_report_data: Dict[str, Optional[DolarBlue]] = {}

    for key in report_data:
        try:
            source = DolarBlueSource(key)
            buy = report_data[key]["buy_price"]
            sell = report_data[key]["sell_price"]
            parsed_report_data[key] = DolarBlue(
                source, buy, sell, datetime.now()
            )

        except KeyError as key_err:
            logging.error("Key Error parsing dictionary: %s", key_err)
            parsed_report_data[key] = None

        except ValueError as value_error:
            logging.error("ValueError parsing dictionary: %s", value_error)
            parsed_report_data[key] = None

        # Just in case something weird happens...
        except Exception as exception:  # pylint: disable=broad-except
            logging.error("Generic error parsing dictionary: %s", exception)
            parsed_report_data[key] = None

    return parsed_report_data


def subscribe_to_cache_updated(handler: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for subscribing a function to the
    'dolarblue-values-updated' channel when said function is called.

    It provides a report to the decorated function, so it MUST accept 'report:Optional[DolarBlue]'
    as a kwarg"""

    @wraps(handler)
    def provider(*args: Any, **kwargs: Any) -> None:
        def values_updated_handler(message: Dict[str, Any]) -> None:

            # Provide the report to the handler
            report_data = parse_json_report(message["data"])

            kwargs["report"] = report_data

            handler(*args, **kwargs)

        subscription_builder("dolarblue-values-updated",
                             values_updated_handler)

    return provider
