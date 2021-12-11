"""Redis database for cache"""
from typing import Any, Dict, Optional
from redis import Redis
from libs.redis_cache.factory import RedisFactory

class RedisDb:
    """Cache databse for storing key value pairs."""
    redis_db: Redis = RedisFactory.build_db()

    @classmethod
    def store_dict(cls, h_name: str, h_dict: Dict[str, Any]) -> None:
        """Stores a dictionary in redis as a hashmap."""
        for key, value in h_dict.items():
            cls.redis_db.hset(h_name, key, value)

    @classmethod
    def get_dict(cls, h_name: str, *args: str) -> Optional[Dict[str, Any]]:
        """Returns a dictionary with all the values found in the redis cache of the element."""

        if not cls.redis_db.exists(h_name):
            return None

        return_dict = {}
        for arg in args:
            return_dict[arg] = cls.redis_db.hget(h_name, arg)
        return return_dict

    @classmethod
    def delete_dict(cls, h_name: str, *args: str) -> None:
        """Deletes all the entries from a hmap in redis for a given key."""

        if not cls.redis_db.exists(h_name):
            return

        cls.redis_db.hdel(h_name, *args)
        cls.redis_db.delete(h_name)