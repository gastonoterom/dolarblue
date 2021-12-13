# pylint: disable=missing-docstring

import unittest
from unittest.mock import patch
from libs.redis_cache.redis_db import RedisDb
from tests.mock_classes.mock_redis import MockRedis


class TestRedisDb(unittest.TestCase):


    @patch("redis.Redis")
    def test_redis_db(self, mock_conn) -> None:

        # Create fake redis connection
        mock_conn = MockRedis()
        RedisDb.redis_conn = mock_conn

        # Store a sample dict
        sample_dict = {
            "buy_price": 100,
            "sell_price": 200
        }

        # Store the dict
        RedisDb.store_dict(
            "agrofy",
            sample_dict
        )

        stored_dict = RedisDb.get_dict("agrofy", "buy_price", "sell_price")

        assert stored_dict is not None
        # Compare the created dict with the stored one
        self.assertDictEqual(stored_dict, sample_dict)

        # Delete the stored dictionary and check for deletion
        RedisDb.delete_dict("agrofy")
        self.assertIsNone(RedisDb.get_dict("agrofy"))

        # Try to delete a not existant dictionary
        self.assertIsNone(RedisDb.delete_dict("mmmmm_aaa"))
