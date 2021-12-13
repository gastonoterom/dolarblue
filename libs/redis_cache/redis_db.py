"""Redis database for cache"""
from typing import Any, Dict, Optional
from redis import Redis
from libs.redis_cache.wrapper import RedisWrapper

class RedisDb:
    """Cache databse for storing key value pairs."""
    redis_conn: Redis = RedisWrapper().get_connection()

    @classmethod
    def store_dict(cls, h_name: str, h_dict: Dict[str, Any]) -> None:
        """Stores a dictionary in redis as a hashmap."""
        for key, value in h_dict.items():
            cls.redis_conn.hset(h_name, key, value)

    @classmethod
    def get_dict(cls, h_name: str, *args: str) -> Optional[Dict[str, Any]]:
        """Returns a dictionary with all the values found in the redis cache of the element."""

        if not cls.redis_conn.exists(h_name):
            return None

        return_dict = {}
        for arg in args:
            return_dict[arg] = cls.redis_conn.hget(h_name, arg)
        return return_dict

    @classmethod
    def delete_dict(cls, h_name: str) -> None:
        """Deletes all the entries from a hmap in redis for a given key."""

        if not cls.redis_conn.exists(h_name):
            return

        cls.redis_conn.delete(h_name)
