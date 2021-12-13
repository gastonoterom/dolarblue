"""Dolar blue parent module."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from classes.dolar_blue import DolarBlue
from libs.redis_cache.redis_db import RedisDb

class DolarBlueSource(ABC):
    """Abstract class for representing a Dolar Blue Source of information."""
    source_name: str
    cache_store: RedisDb = RedisDb()

    def __init__(
        self,
        source_name:str,
        cache_store: Optional[RedisDb] = None
    ):
        self.source_name = source_name

        if cache_store:
            self.cache_store = cache_store
        else:
            self.cache_store = RedisDb()

    @abstractmethod
    def get_blue(self) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""
        # Subclass responsability: ScrapingSource, RestApiSource or XmlSource

    def get_cached_blue(self) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from cache."""

        dolarblue_dict = self.cache_store.get_dict(
            self.source_name, "buy_price", "sell_price", "date_time"
        )

        if dolarblue_dict is None:
            return None

        return DolarBlue(
            source = self.source_name,
            buy_price = float(dolarblue_dict["buy_price"]),
            sell_price = float(dolarblue_dict["sell_price"]),
            date_time = datetime.strptime(str(dolarblue_dict["date_time"]), "%m-%d-%Y %H:%M:%S"),
        )

    def set_blue_in_cache(self, dolarblue: DolarBlue) -> None:
        """Cache the dolar blue value to redis."""

        dolarblue_dict = dolarblue.to_dict()

        # Average price is calculated so storing it is unnecessary
        del dolarblue_dict["average_price"]

        self.cache_store.store_dict(self.source_name, dolarblue.to_dict())

    def erase_blue_in_cache(self) -> None:
        """Erase the dolarblue value in redis."""
        self.cache_store.delete_dict(self.source_name)

    def update_cache(self) -> bool:
        """Updates and sets the cache and prevcache for the dolar price in redis. Returns True
        if update was successful or False if it failed"""

        # Fetching dolar blue value from source
        dolarblue = self.get_blue()

        # Adding the latest dolarblue in cache if found
        if dolarblue:
            self.erase_blue_in_cache()
            self.set_blue_in_cache(dolarblue)
            return True

        return False
