from __future__ import annotations
from datetime import datetime
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple
from src.libs.custom_exceptions.fetching_exception import FetchingException
from src.libs.redis_cache.redis_db import RedisDb


@dataclass
class DolarBlue:
    """Dolarblue class: links a source to a buying and selling price."""

    source: DolarBlueSource
    buy_price: float
    sell_price: float
    date_time: datetime = datetime.now()

    @property
    def average(self) -> float:
        """Calculate the average between the sell and buy price"""
        return round((self.buy_price + self.sell_price) / 2, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Returns the dolarblue object as a JSON serializable dictionary."""

        return {
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "average_price": self.average,
            "date_time": self.date_time.strftime("%m-%d-%Y %H:%M:%S")
        }


class DolarBlueSource:
    """Class that represents a Dolar Blue Source of information.

    This class represents for example a scrapable website, a rest api or an xml api
    where we can get dolarblue values from. An example would be any major Argentinian newspaper."""

    def __init__(
            self,
            source_name: str,
            fetching_strategy: Optional[Callable[[],
                                                 Tuple[float, float]]] = None,
            cache_store: Optional[RedisDb] = None
    ):
        """Constructor for a DolarBlueSource of information.

        The source name is a representative string of the name of the site or API.
        The fetching strategy is a callable that returns two floats, the BUY and the SELL
        price of the source, its internal composition is irrelevant
        for this class as long as it returns a tuple of two floats.
        The cache store is a place to store the fetched values for quick access,
        it can be a redis database or any other key value store, in the future it's type should
        be a protocol that complies with the required functions"""

        self.source_name = source_name
        self.fetching_strategy = fetching_strategy
        self.cache_store = cache_store if cache_store else RedisDb()

    def get_blue(self) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source, if possible.

        This function executes the fetching function given when instantiating
        the object, and then returns a DolarBlue object from its returning values. If the fetching
        function fails, it logs the exception and returns None."""
        if self.fetching_strategy is None:
            return None

        try:

            buy_price, sell_price = self.fetching_strategy()

            return DolarBlue(
                source=self,
                buy_price=buy_price,
                sell_price=sell_price,
            )

        except FetchingException as fep:
            logging.error(fep)
            logging.error("Error fetching %s dolar blue value",
                          self.source_name)
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
            source=self,
            buy_price=float(dolarblue_dict["buy_price"]),
            sell_price=float(dolarblue_dict["sell_price"]),
            date_time=datetime.strptime(
                str(dolarblue_dict["date_time"]), "%m-%d-%Y %H:%M:%S"),
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

    def update_cache(self) -> Optional[DolarBlue]:
        """Updates the cache of the DolarBlueSource if a new value is found.
        Returns a bool representing it's success or failure."""

        logging.info("Starting cache update for %s", self.source_name)

        dolarblue = self.get_blue()

        if dolarblue:
            self.erase_blue_in_cache()
            self.set_blue_in_cache(dolarblue)
            logging.info("Cache update for %s was successful",
                         self.source_name)
            return dolarblue

        logging.info("Cache update for %s was a failure", self.source_name)
        return None
