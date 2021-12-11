"""Factory for redis cache objects"""

from redis import Redis

from consts.redis import REDIS_DB, REDIS_HOST, REDIS_PORT

class RedisFactory:
    """Factory redis for Redis cache objects."""

    @staticmethod
    def build_db() -> Redis:
        """Builds and returns a Redis object for database connection"""
        return Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB )
