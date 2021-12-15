# pylint: disable=missing-docstring

import unittest
from redis import Redis
from libs.redis_cache.wrapper import RedisWrapper
from tests.testing_consts import REDIS_TEST_DB, REDIS_TEST_HOST, REDIS_TEST_PORT

class TestRedisWrapper(unittest.TestCase):

    def test_redis_wrapper(self) -> None:

        redis_default_w = RedisWrapper()
        self.assertIsNotNone(redis_default_w.redis_db)

        redis_conn = Redis(
            host=REDIS_TEST_HOST,
            port=REDIS_TEST_PORT,
            db=REDIS_TEST_DB,
            decode_responses=True,
            encoding="utf-8"
        )

        redis_w = RedisWrapper(
            redis_conn
        )

        redis_db = redis_w.get_connection()
        redis_db.ping()
        self.assertEqual(type(redis_db), Redis)
