"""Dolar blue parent module."""

from abc import abstractmethod
from datetime import datetime
from typing import Optional
from classes.dolar_blue import DolarBlue
from libs.redis_cache.redis_db import RedisDb

class DolarBlueSource():
    """Class for representing a Dolar Blue Source of information."""
    source_name: str
    cache_store: RedisDb = RedisDb()

    @classmethod
    @abstractmethod
    def get_blue(cls) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""
        # Subclass responsability: scraping_source, rest_api_source or xml_source

    @classmethod
    def get_cached_blue(cls) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from cache."""
        dolarblue_dict = cls.cache_store.get_dict(
            cls.source_name, "buy_price", "sell_price", "date_time"
        )

        if dolarblue_dict is None:
            return None

        return DolarBlue(
            source = cls.source_name,
            buy_price = float(dolarblue_dict["buy_price"]),
            sell_price = float(dolarblue_dict["sell_price"]),
            date_time = datetime.strptime(str(dolarblue_dict["date_time"]), "%m-%d-%Y %H:%M:%S"),
        )

    @classmethod
    def set_blue_in_cache(cls, dolarblue: DolarBlue) -> None:
        """Cache the dolar blue value to redis."""
        dolarblue_dict = dolarblue.to_dict()
        # Average price is calculated so storing it is unnecessary
        del dolarblue_dict["average_price"]
        cls.cache_store.store_dict(cls.source_name, dolarblue.to_dict())

    @classmethod
    def erase_blue_in_cache(cls) -> None:
        """Erase the dolarblue value in redis."""
        cls.cache_store.delete_dict(cls.source_name, "buy_price", "sell_price", "date_time")

    @classmethod
    def update_cache(cls) -> bool:
        """Updates and sets the cache and prevcache for the dolar price in redis. Returns True
        if update was successful or False if it failed"""

        # Fetching dolar blue value from source
        dolarblue = cls.get_blue()

        # Adding the latest dolarblue in cache if found
        if dolarblue:
            cls.erase_blue_in_cache()
            cls.set_blue_in_cache(dolarblue)
            return True

        return False
