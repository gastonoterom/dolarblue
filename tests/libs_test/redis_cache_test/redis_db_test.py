# pylint: disable=missing-docstring

import unittest
import redis
from libs.redis_cache.redis_db import RedisDb
from tests.testing_consts import REDIS_TEST_DB, REDIS_TEST_HOST, REDIS_TEST_PORT


class TestRedisDb(unittest.TestCase):

    def test_redis_db(self) -> None:
        # Create and replace the test redis connection

        RedisDb.redis_conn = redis.Redis(
            host=REDIS_TEST_HOST,
            port=REDIS_TEST_PORT,
            db=REDIS_TEST_DB,
            decode_responses=True,
            encoding="utf-8"
        )

        RedisDb.redis_conn.ping()

        # Store a sample dict
        sample_dict = {
            "value_one": "one",
            "value_two": "two",
        }

        # Store the dict
        RedisDb.store_dict(
            "test_dict",
            sample_dict
        )

        stored_dict = RedisDb.get_dict("test_dict", "value_one", "value_two", "not_in_dict")

        assert stored_dict is not None
        assert "not_in_dict" not in stored_dict

        # Compare the created dict with the stored one
        self.assertDictEqual(stored_dict, sample_dict)

        # Delete the stored dictionary and check for deletion
        RedisDb.delete_dict("test_dict")
        self.assertIsNone(RedisDb.get_dict("test_dict"))

        # Try to delete a not existant dictionary
        self.assertIsNone(RedisDb.delete_dict("mmmmm_aaa"))
