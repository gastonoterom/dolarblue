# pylint: disable=missing-docstring

import unittest
from redis import Redis
from libs.redis_cache.wrapper import RedisWrapper
from tests.testing_consts import REDIS_TEST_DB, REDIS_TEST_HOST, REDIS_TEST_PORT

class TestRedisWrapper(unittest.TestCase):

    def test_wrapper(self) -> None:

        redis_w = RedisWrapper(
            host=REDIS_TEST_HOST,
            port=REDIS_TEST_PORT,
            db_num=REDIS_TEST_DB
        )

        redis_db = redis_w.get_connection()
        redis_db.ping()
        self.assertEqual(type(redis_db), Redis)
