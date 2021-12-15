import json
import logging
from asyncio import sleep
from typing import Callable, Any

from src.classes import DolarBlueSource
from src.libs.redis_cache.redis_pub_sub import RedisSub
from src.pub_sub.publishers.update_values_pub import pub_values_updated


def subscription_builder(channel:str , handler: Callable[[dict], None]) -> RedisSub:
    redis_sub = RedisSub()
    redis_sub.subscribe(channel, handler)

    return redis_sub


def sub_update_values() -> RedisSub:
    def update_values_handler(_: dict) -> None:
        logging.info("Updating dolar blue values.")
        updated_sources = DolarBlueSource.update_all()
        pub_values_updated(updated_sources)

    return subscription_builder("update-dolarblue-values", update_values_handler)


def sub_values_updated(handler: Callable[[dict[str, bool]], Any]) -> RedisSub:
    def values_updated_handler(message_info: dict) -> None:
        report_data: dict[str, bool] = json.loads(message_info["data"])
        handler(report_data)

    return subscription_builder("dolarblue-values-updated",values_updated_handler)
