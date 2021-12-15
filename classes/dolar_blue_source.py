"""Dolar blue parent module."""

from __future__ import annotations
from datetime import datetime
import logging
from typing import Callable, List, Optional, Tuple
from classes.dolar_blue import DolarBlue
from libs.custom_exceptions.fetching_exception import FetchingException
from libs.redis_cache.redis_db import RedisDb
from libs.scraping.dolar_blue_sources.agrofy.utils import scrape_agrofy_values
from libs.scraping.dolar_blue_sources.dolarhoy.utils import scrape_dolarhoy_values
from libs.scraping.dolar_blue_sources.infodolar.utils import scrape_infodolar_values

class DolarBlueSource():
    """Class that represents a Dolar Blue Source of information."""

    @staticmethod
    def get_all() -> List[DolarBlueSource]:
        """Gets all the existant dolar blue sources."""
        return [
            DolarBlueSource(source_name="agrofy", fetching_function=scrape_agrofy_values),
            DolarBlueSource(source_name="infodolar", fetching_function=scrape_infodolar_values),
            DolarBlueSource(source_name="dolarhoy", fetching_function=scrape_dolarhoy_values,),
    ]

    source_name: str
    cache_store: RedisDb = RedisDb()

    def __init__(
            self,
            source_name:str,
            fetching_function: Callable[[], Tuple[int,int]],
            cache_store: Optional[RedisDb] = None
        ):

        self.source_name = source_name
        self.fetching_function = fetching_function
        self.cache_store = cache_store if cache_store else RedisDb()

    def get_blue(self) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""
        try:

            buy_price, sell_price = self.fetching_function()

            return DolarBlue(
                source=self.source_name,
                buy_price=buy_price,
                sell_price=sell_price,
            )

        except FetchingException as fep:
            logging.error(fep)
            logging.error("Error fetching %s dolar blue value", self.source_name)
            return None


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
