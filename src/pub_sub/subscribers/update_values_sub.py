import json
from typing import Callable, Any
from src.libs.redis_cache.redis_pub_sub import RedisSub


def subscription_builder(channel:str , handler: Callable[[Any], None]) -> RedisSub:
    redis_sub = RedisSub()
    redis_sub.subscribe(channel, handler)

    return redis_sub

def subscribe_to_update_request(handler: Callable) -> Callable:
    """Subscribe a function to the update request channel"""
    def injector() -> None:
        def update_request_handler(_: Any):

            handler()

        subscription_builder("update-dolarblue-values", update_request_handler)
    return injector


def subscribe_to_cache_updated(handler: Callable) -> Callable:
    """Handler function MUST have 'report' as a kwarg, or this function will
    fail, it will inject the report in that argument."""
    def injector(*args, **kwargs) -> None:
        def values_updated_handler(message: dict) -> None:

            report_data: dict[str, bool] = json.loads(message["data"])
            kwargs["report"] = report_data

            handler(*args, **kwargs)

        subscription_builder("dolarblue-values-updated", values_updated_handler)
    return injector
