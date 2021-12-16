from typing import Any, Dict, Optional
from redis import Redis
from src.libs.redis_cache.wrapper import RedisWrapper


class RedisDb:
    """Redis cache database for storing key value pairs."""

    redis_conn: Redis

    def __init__(self, redis_conn: Optional[Redis] = None):
        """Initialize the redis database.

        Gets a connection from the projects main pool if no particular connection is specified."""

        self.redis_conn = redis_conn if redis_conn else RedisWrapper().get_connection()

    def store_dict(self, h_name: str, h_dict: Dict[str, Any]) -> None:
        """Stores a dictionary in redis as a hashmap, key values must be primitive values."""

        for key, value in h_dict.items():
            self.redis_conn.hset(h_name, key, value)

    def get_dict(self, h_name: str, *args: str) -> Optional[Dict[str, str]]:
        """Returns a dictionary with all the values found in the redis cache of the element.
        Returns None if the key is not on the store.

        Dictionary values should be parsed into other types
        as the business logic requires."""

        if not self.redis_conn.exists(h_name):
            return None

        return_dict: Dict[str, str] = {}

        for arg in args:
            val = self.redis_conn.hget(h_name, arg)
            if val:
                return_dict[arg] = str(self.redis_conn.hget(h_name, arg))

        return return_dict

    def delete_dict(self, h_name: str) -> None:
        """Deletes all the entries from a hash map in redis for a given key."""

        if not self.redis_conn.exists(h_name):
            return

        self.redis_conn.delete(h_name)
