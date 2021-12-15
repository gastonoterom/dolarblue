import json
from typing import Callable, Any
from src.libs.redis_cache.redis_pub_sub import RedisSub


def subscription_builder(channel:str , handler: Callable[[Any], None]) -> RedisSub:
    redis_sub = RedisSub()
    redis_sub.subscribe(channel, handler)

    return redis_sub

def dolarblue_cache_update_request(handler: Callable[[None], None]) -> RedisSub:
    return subscription_builder("update-dolarblue-values", handler)


def dolarblue_cache_updated(handler: Callable[[dict[str, bool]], None]) -> RedisSub:
    def values_updated_handler(message_info: dict) -> None:
        report_data: dict[str, bool] = json.loads(message_info["data"])
        handler(report_data)

    return subscription_builder("dolarblue-values-updated",values_updated_handler)
