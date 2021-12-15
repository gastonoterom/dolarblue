import json

from src.libs.redis_cache.redis_pub_sub import RedisPub


def publish_function(chann:str, *args) -> None:
    redis_pub = RedisPub()
    redis_pub.publish(chann, *args)


def pub_update_values() -> None:
    publish_function("update-dolarblue-values", "update-request")


def pub_values_updated(sources_updated: dict) -> None:
    publish_function("dolarblue-values-updated", json.dumps(sources_updated))
