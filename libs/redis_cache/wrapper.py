"""Wrapper for redis cache objects"""

from typing import Optional
from redis import Redis
from libs.redis_cache.config import REDIS_DB, REDIS_HOST, REDIS_PORT

default_redis_db = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    encoding="utf-8"
)

class RedisWrapper:
    """Redis wrapper"""

    def __init__(
            self,
            redis_db: Optional[Redis] = None
        ):

        """Initialize a redis wrapper with connection setting values"""
        self.redis_db = redis_db if redis_db else default_redis_db

    def get_connection(self) -> Redis:
        """Gets a redis connection from the wrapper"""
        return self.redis_db
