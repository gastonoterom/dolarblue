# pylint: disable=missing-docstring

import unittest
import redis
from src.libs.redis_cache.redis_db import RedisDb
from tests.testing_consts import REDIS_TEST_DB, REDIS_TEST_HOST, REDIS_TEST_PORT


class TestRedisDb(unittest.TestCase):

    def test_redis_db(self) -> None:
        # Create and replace the test redis connection
        redis_db_empty = RedisDb()
        self.assertIsInstance(redis_db_empty.redis_conn, redis.Redis)

        redis_db = RedisDb(
            redis.Redis(
                host=REDIS_TEST_HOST,
                port=REDIS_TEST_PORT,
                db=REDIS_TEST_DB,
                decode_responses=True,
                encoding="utf-8"
            )
        )

        redis_db.redis_conn.ping()

        # Store a sample dict
        sample_dict = {
            "value_one": "one",
            "value_two": "two",
        }

        # Store the dict
        redis_db.store_dict(
            "test_dict",
            sample_dict
        )

        stored_dict = redis_db.get_dict("test_dict", "value_one", "value_two", "not_in_dict")

        assert stored_dict is not None
        assert "not_in_dict" not in stored_dict

        # Compare the created dict with the stored one
        self.assertDictEqual(stored_dict, sample_dict)

        # Delete the stored dictionary and check for deletion
        redis_db.delete_dict("test_dict")
        self.assertIsNone(redis_db.get_dict("test_dict"))

        # Try to delete a not existant dictionary
        redis_db.delete_dict("mmmmm_aaa")
