"""Dolar blue scraping parent module."""

from typing import Callable, Optional, Tuple
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from classes.dolar_blue import DolarBlue
from classes.dolar_blue_source import DolarBlueSource
from libs.scraping.exceptions.scraping_error import ScrapingException
from libs.scraping.scrape_page import scrape_dolar_values_from_source
from main import flask_logger

class ScrapingSource(DolarBlueSource):
    """Class for representing a Dolar Blue NON rest-api scrapable Source of information."""

    selenium_fetching: Callable[[WebDriver], str]
    soup_scraping: Callable[[BeautifulSoup], Tuple[float, float]]


    @classmethod
    def get_blue(cls) -> Optional[DolarBlue]:
        """Fetch and return the dolar blue value from the source."""

        try:
            return scrape_dolar_values_from_source(
                cls.source_name,
                cls.selenium_fetching,
                cls.soup_scraping
            )

        except ScrapingException as scep:
            flask_logger.error(scep)
            flask_logger.error("Error fetching %s dolar blue value", cls.source_name)
            return None
