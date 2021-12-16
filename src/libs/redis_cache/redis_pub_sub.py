from __future__ import annotations
from typing import Any, Optional, Callable, List
from redis import Redis
from redis.client import PubSub, PubSubWorkerThread
from src.libs.custom_exceptions.redis_exceptions import SubscriptionNotFoundException
from src.libs.redis_cache.utils import needs_open_connection
from src.libs.redis_cache.wrapper import RedisWrapper


class RedisSub:
    """Redis class for a subscription object.

    Sub objects are created as 'opened', and can only be closed once. From that point on,
    they cannot be opened for subscribing anymore."""

    redis_pubsub: PubSub
    threads: dict[str, List[PubSubWorkerThread]] = {}
    closed: bool = False

    def __init__(
            self,
            redis_pubsub: Optional[PubSub] = None,
    ):
        """Needs a redis lower level pubsub object,
        if none is provided one is obtained from the projects pool factory"""
        self.redis_pubsub = redis_pubsub if redis_pubsub else \
            RedisWrapper().get_connection().pubsub(ignore_subscribe_messages=True)

    @needs_open_connection
    def subscribe(self, chann: str, handler: Callable[[Any], Any]) -> None:
        """Subscribes the redis pubsub object to a specified channel with a handler function,
        requires an open pubsub connection."""

        self.redis_pubsub.subscribe(**{chann: handler})

        if self.threads.get(chann) is None:
            self.threads[chann] = []

        self.threads[chann].append(
            self.redis_pubsub.run_in_thread(sleep_time=0.001))

    @needs_open_connection
    def unsubscribe_all(self) -> None:
        """Unsubscribe all subscribers from the pubsub object

        This function also stops all the threads and deletes them."""

        self.redis_pubsub.unsubscribe()

        for thread_list in self.threads.values():
            for thread in thread_list:
                thread.stop()

        self.threads = {}

    @needs_open_connection
    def unsubscribe(self, chann: str) -> None:
        """Unsubscribe all the subscribers for a specific channel provided.
        Also stops all their respective threads.

        The object must have previously been subscribed or
        it will raise a SubscriptionNotFoundException."""

        if self.threads.get(chann) is None:
            raise SubscriptionNotFoundException(f"Can't unsubscribe from {chann} \
                as it was never subscribed to")

        self.redis_pubsub.unsubscribe(chann)
        for thread in self.threads[chann]:
            thread.stop()

        del self.threads[chann]

    def close(self) -> None:
        """Close the pubsub object, this action is irreversible."""
        self.redis_pubsub.close()
        self.threads = {}
        self.closed = True


class RedisPub:
    """Class for publishing events on redis."""

    redis_conn: Redis[str]

    def __init__(
            self,
            redis_conn: Optional[Redis[str]] = None,
    ):
        """Needs a redis connection, if
        none is provided one is obtained from the projects factory"""
        self.redis_conn = redis_conn if redis_conn else RedisWrapper().get_connection()

    def publish(self, chann: str, *args: Any) -> None:
        """Publish a message to a specified channel"""
        self.redis_conn.publish(chann, *args)
