# pylint: disable=missing-docstring

import unittest
from redis import Redis
from libs.redis_cache.wrapper import RedisWrapper

class TestRedisWrapper(unittest.TestCase):

    def test_wrapper(self) -> None:

        redis_w = RedisWrapper()
        redis_db = redis_w.get_connection()
        self.assertEqual(type(redis_db), Redis)
