"""Redis wrapper for publishers and subscribers"""

from typing import Optional, Callable
from redis import Redis
from redis.client import PubSub, PubSubWorkerThread
from src.libs.redis_cache.wrapper import RedisWrapper


class RedisSub:
    """Redis subscription class."""

    redis_pubsub: PubSub
    threads: dict[str, PubSubWorkerThread]

    def __init__(
            self,
            redis_pubsub: Optional[PubSub] = None,
    ):
        self.redis_pubsub = redis_pubsub if redis_pubsub else \
            RedisWrapper().get_connection().pubsub(ignore_subscribe_messages=True)
        self.threads = {}

    def stop(self):
        self.redis_pubsub.unsubscribe()
        for thread in self.threads.values():
            thread.stop()

    def subscribe(self, chann: str, handler: Callable):
        """Subscribes the redis pubsub object to a specified channel with a handler"""
        self.redis_pubsub.subscribe(**{chann: handler})
        self.threads[chann] = self.redis_pubsub.run_in_thread(sleep_time=0.001)

    def unsubscribe(self, chann: str):
        self.unsubscribe(chann)
        self.threads[chann].stop()


class RedisPub:
    """Redis publisher class."""

    redis_conn: Redis

    def __init__(
            self,
            redis_conn: Optional[Redis] = None,
    ):
        self.redis_conn = redis_conn if redis_conn else RedisWrapper().get_connection()

    def publish(self, chann: str, *args):
        """Publish a message to a specified channel"""
        self.redis_conn.publish(chann, *args)
