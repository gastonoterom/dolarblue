"""Dolar blue scraping parent module."""

from typing import Any, Callable, Optional, Tuple
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from classes.dolar_blue import DolarBlue
from classes.dolar_blue_source import DolarBlueSource
from consts.selenium import REMOTE_SELENIUM_URL
from libs.redis_cache.redis_db import RedisDb
from libs.scraping.exceptions.scraping_error import ScrapingException
from libs.scraping.scrape_page import scrape_dolar_values_from_source
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory

def selenium_injection(
        selenium_requirer: Callable[
            [
                Any,
                Optional[WebDriver]
            ],
            Optional[Any]]
        ):
    """Selenium driver injector for instance function that requires it."""

    def inject_driver(self, driver: Optional[WebDriver] = None) -> Optional[DolarBlue]:
        if driver is None:
            driver = SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL)
        response = selenium_requirer(self, driver)
        if driver:
            driver.close()
            driver.quit()
        return response

    return inject_driver

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
            return scrape_dolar_values_from_source(
                self.source_name,
                self.selenium_fetching,
                self.soup_scraping,
                driver
            )

        except ScrapingException as scep:
            logging.error(scep)
            logging.error("Error fetching %s dolar blue value", self.source_name)
            return None

    def get_blue(self):
        """Fetch and return the scraped dolar blue value from the source."""
        return self.get_scraped_blue()
