"""Wrapper for redis cache objects"""

import logging
from typing import Optional
from redis import Redis
import redis
from consts.redis import REDIS_DB, REDIS_HOST, REDIS_PORT

class RedisWrapper:
    """Redis wrapper"""

    def __init__(
            self,
            host: Optional[str]=None,
            db_num: Optional[int]=None,
            port: Optional[int]=None
        ):

        """Initialize a redis wrapper with connection setting values"""
        if host:
            self.host = host
        else:
            self.host = REDIS_HOST

        if db_num:
            self.db_num = db_num
        else:
            self.db_num = REDIS_DB

        if port:
            self.port = port
        else:
            self.port = REDIS_PORT

    def get_connection(self) -> Redis:
        """Builds and returns a Redis object for database connection"""
        logging.info("Getting connection from redis")
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db_num,
            decode_responses=True,
            encoding="utf-8"
        )
