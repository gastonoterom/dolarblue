"""Redis wrapper for publishers and subscribers"""

from typing import Optional, Callable, List
from redis import Redis
from redis.client import PubSub, PubSubWorkerThread
from src.libs.redis_cache.wrapper import RedisWrapper


def needs_open_connection(validated_function: Callable):
    def check_connection(self, *args, **kwargs):
        if self.closed:
            raise Exception("ERROR: Cant perform operation on closed pubsub.")

        return validated_function(self, *args, **kwargs)

    return check_connection

class RedisSub:
    """Redis subscription class."""

    redis_pubsub: PubSub
    threads: dict[str, List[PubSubWorkerThread]] = {}
    closed: bool = False
    def __init__(
            self,
            redis_pubsub: Optional[PubSub] = None,
    ):
        self.redis_pubsub = redis_pubsub if redis_pubsub else \
            RedisWrapper().get_connection().pubsub(ignore_subscribe_messages=True)

    @needs_open_connection
    def unsubscribe_all(self):
        self.redis_pubsub.unsubscribe()
        for thread_list in self.threads.values():
            for thread in thread_list:
                thread.stop()
        self.threads = {}

    @needs_open_connection
    def subscribe(self, chann: str, handler: Callable):
        """Subscribes the redis pubsub object to a specified channel with a handler"""

        self.redis_pubsub.subscribe(**{chann: handler})
        if self.threads.get(chann) is None:
            self.threads[chann] = []

        self.threads[chann].append(self.redis_pubsub.run_in_thread(sleep_time=0.001))

    @needs_open_connection
    def unsubscribe(self, chann: str):
        if self.threads.get(chann) is None:
            raise Exception("Can't unsubscribe from channel %s as it was never subscribed to", chann)

        self.redis_pubsub.unsubscribe(chann)
        for thread in self.threads[chann]:
            thread.stop()
        del self.threads[chann]

    def close(self):
        self.redis_pubsub.close()
        self.threads = {}
        self.close = True

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
