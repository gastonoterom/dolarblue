import json
from typing import Dict, Optional
from src.classes.dolar_blue import DolarBlue
from src.libs.redis_cache.redis_pub_sub import RedisPub


def publish_function(chann: str, message: str) -> None:
    """Published a message to a specified channel.."""

    redis_pub = RedisPub()
    redis_pub.publish(chann, message)


def pub_update_values() -> None:
    """Publishes a 'update-dolarblue-values'
    with an 'update-request' message to the pubsub manager."""

    publish_function("update-dolarblue-values", "update-request")


def pub_values_updated(sources_updated: Dict[str, Optional[DolarBlue]]) -> None:
    """Publishes a 'dolarblue-values-updated' message
    to the pubsub manager, with the sources updated information as a JSON serialized message.

    The argument sources_updated MUST be JSON serializable or the function raises a TypeError"""

    try:
        json_payload = json.dumps({
            src: None if val is None else val.to_dict()
            for src, val
            in sources_updated.items()
        })

    except Exception as error:
        raise TypeError(
            "sources_update dictionary is NOT json serializable") from error

    publish_function("dolarblue-values-updated", json_payload)
