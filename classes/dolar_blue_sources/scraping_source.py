"""Dolar blue scraping parent module."""

from typing import Callable, Optional, Tuple
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from classes.dolar_blue import DolarBlue
from classes.dolar_blue_source import DolarBlueSource
from libs.redis_cache.redis_db import RedisDb
from libs.scraping.exceptions.scraping_error import ScrapingException
from libs.scraping.scrape_page import scrape_dolar_values_from_source
from libs.scraping.utils import selenium_injection

class DolarScrapingSource(DolarBlueSource):
    """Class for representing a Dolar Blue NON rest-api scrapable Source of information."""

    def __init__(
        self,
        source_name:str,
        selenium_fetching: Callable[[WebDriver], str],
        soup_scraping: Callable[[BeautifulSoup], Tuple[float, float]],
        cache_store:Optional[RedisDb] = None,
    ):
        super().__init__(source_name, cache_store)
        self.selenium_fetching = selenium_fetching
        self.soup_scraping = soup_scraping

    @selenium_injection
    def get_scraped_blue(self, driver: Optional[WebDriver] = None) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""
        try:
            assert driver is not None

            buy_price, sell_price = scrape_dolar_values_from_source(
                self.selenium_fetching,
                self.soup_scraping,
                driver
            )

            return DolarBlue(
                source=self.source_name,
                buy_price=buy_price,
                sell_price=sell_price,
            )

        except ScrapingException as scep:
            logging.error(scep)
            logging.error("Error fetching %s dolar blue value", self.source_name)
            return None

    def get_blue(self):
        """Fetch and return the scraped dolar blue value from the source."""
        # The selenium driver is injected by the decorator
        return self.get_scraped_blue()
