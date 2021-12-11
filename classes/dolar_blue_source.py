"""Dolar blue parent module."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, cast
from classes.dolar_blue import DolarBlue
from libs.redis_cache.redis_db import redis_db

class DolarBlueSource(ABC):
    """Abstract class for representing a Dolar Blue Source of information."""
    source_name: str

    @staticmethod
    @abstractmethod
    def get_blue() -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""

    @classmethod
    def __get_cached(cls, h_name: str) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from cache."""
        if not redis_db.exists(h_name):
            return None

        buy_price = cast(float,redis_db.hget(h_name, "buy"))
        sell_price = cast(float,redis_db.hget(h_name, "sell"))
        date_time = cast(float, redis_db.hget(h_name, "date_time"))
        
        return DolarBlue(cls.source_name, buy_price, sell_price,
            datetime.fromtimestamp(float(date_time)))

    @classmethod
    def __set_cached(cls, h_name: str, dolarblue: DolarBlue) -> None:
        """Fetch and return the dolar blue value from cache."""
        redis_db.hset(h_name, "buy", dolarblue.buy_price)
        redis_db.hset(h_name, "sell", dolarblue.sell_price)
        redis_db.hset(h_name, "date_time", dolarblue.date_time.timestamp())

    @classmethod
    def get_cached_blue(cls) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from cache."""
        return cls.__get_cached(cls.source_name)

    @classmethod
    def get_prev_cached_blue(cls) -> Optional[DolarBlue]:
        """Fetch and return the previously working dolar blue value from cache."""
        return cls.__get_cached(cls.source_name + "_prev")

    @classmethod
    def set_blue_in_cache(cls, dolarblue: DolarBlue) -> None:
        """Cache the dolar blue value to redis."""
        cls.__set_cached(cls.source_name, dolarblue)

    @classmethod
    def set_prev_blue_in_cache(cls, dolarblue: DolarBlue) -> None:
        """Cache the dolar blue value to redis."""
        cls.__set_cached(cls.source_name + "_prev", dolarblue)

    @classmethod
    def erase_blue_in_cache(cls) -> None:
        """Erase the dolarblue value in redis."""
        if not redis_db.exists(cls.source_name):
            return None

        redis_db.hdel(cls.source_name)

    @classmethod
    def update_cache(cls) -> None:
        """Updates and sets the cache and prevcache for the dolar price in redis."""

        # Fetching last redis value from store
        dolarblue_cached = cls.get_cached_blue()

        # Saving last redis value from store to previous value in store if not None
        if dolarblue_cached:
            cls.set_prev_blue_in_cache(dolarblue_cached)

        # Fetching dolar blue value from source
        dolarblue = cls.get_blue()

        # Saving dolar blue value from source to redis, or None if error
        if dolarblue:
            cls.set_blue_in_cache(dolarblue)
        else:
            cls.erase_blue_in_cache()
