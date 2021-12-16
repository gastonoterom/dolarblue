from __future__ import annotations
from datetime import datetime
import logging
from time import sleep
from typing import Callable, List, Optional, Tuple
from src.classes.dolar_blue import DolarBlue
from src.libs.custom_exceptions.fetching_exception import FetchingException
from src.libs.redis_cache.redis_db import RedisDb
from src.libs.scraping.dolar_blue_sources.agrofy.utils import scrape_agrofy_values
from src.libs.scraping.dolar_blue_sources.dolarhoy.utils import scrape_dolarhoy_values
from src.libs.scraping.dolar_blue_sources.infodolar.utils import scrape_infodolar_values


class DolarBlueSource:
    """Class that represents a Dolar Blue Source of information.

    This class represents for example a scrapable sebsite, a rest api or an xml api
    where we can get dolarblue values from. An example would be any major Argentinian newspaper."""

    @staticmethod
    def get_all() -> List[DolarBlueSource]:
        """Gets all the existent dolar blue sources."""
        return [
            DolarBlueSource(source_name="agrofy", fetching_function=scrape_agrofy_values),
            DolarBlueSource(source_name="infodolar", fetching_function=scrape_infodolar_values),
            DolarBlueSource(source_name="dolarhoy", fetching_function=scrape_dolarhoy_values,),
        ]

    @staticmethod
    def update_all() -> dict[str, bool]:
        """Updates all the DolarBlue values in the cache store, returns a dict of source names and their respective
        valid update or failure."""

        updated_sources: dict = {}

        for src in DolarBlueSource.get_all():

            success = src.update_cache()
            if success:
                logging.info("Success updating %s values", src.source_name)
                updated_sources[src.source_name] = True

            else:
                logging.info("Failure updating %s values", src.source_name)
                updated_sources[src.source_name] = False

        return updated_sources

    def __init__(
            self,
            source_name:str,
            fetching_function: Callable[[], Tuple[int,int]],
            cache_store: Optional[RedisDb] = None
    ):
        """Constructor for a DolarBlueSource of information.

        The source name is a representative string of the name of the site or API.
        The fetching function is a callable that returns two floats, the BUY and the SELL
        price of the source, its internal composition is irrelevant for this class as long as it returns a tuple of
        two floats.
        The cache store is a place to store the fetched values for quick access, it can be a redis database or any
        other key value store, in the future it's type should be a protocol that complies with the required functions"""

        self.source_name = source_name
        self.fetching_function = fetching_function
        self.cache_store = cache_store if cache_store else RedisDb()

    def get_blue(self) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source, if possible.

        This function executes the fetching function given when instantiating the object, and then returns a DolarBlue
        object from its returning values. If the fetching function fails, it logs the exception and returns None."""

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
        """Fetch and return the dolar blue value from cache, if found.

        If the dolarblue value is not stored in the cache store, it returns none."""

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
        """Save the dolar blue value to the cache store."""

        dolarblue_dict = dolarblue.to_dict()
        # Average price is calculated so storing it is unnecessary
        del dolarblue_dict["average_price"]
        self.cache_store.store_dict(self.source_name, dolarblue.to_dict())

    def erase_blue_in_cache(self) -> None:
        """Erase the dolarblue value in the cache store.

        This function is mainly used to clear the cache when the new values are fetched."""
        self.cache_store.delete_dict(self.source_name)

    def update_cache(self) -> bool:
        """Updates the cache of the DolarBlueSource if a new value is found. Returns a bool representing it's success
        or failure."""

        dolarblue = self.get_blue()
        if dolarblue:
            self.erase_blue_in_cache()
            self.set_blue_in_cache(dolarblue)
            return True

        return False
