"""Wrapper for redis cache objects"""

from redis import Redis
import redis
from main import flask_logger
from consts.redis import REDIS_DB, REDIS_HOST, REDIS_PORT    

class RedisWrapper:
    """Redis wrapper"""

    def get_connection(self) -> Redis:
        """Builds and returns a Redis object for database connection"""
        flask_logger.info("Getting connection from redis")
        return redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            charset="utf-8"
        )
