"""Redis database for cache"""
from libs.redis_cache.factory import RedisFactory

redis_db = RedisFactory.build_db()
