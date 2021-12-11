"""Module that fetches Agrofy dolar blue values from cache or site."""

from typing import Optional
import logging
from classes.dolar_blue import DolarBlue
from classes.dolar_blue_source import DolarBlueSource
from libs.scraping.agrofy.utils import agrofy_soup_scraping, agrofy_selenium_fetching
from libs.scraping.exceptions.scraping_error import ScrapingException
from libs.scraping.scrape_page import scrape_dolar_values_from_source


class Agrofy(DolarBlueSource):
    """Class for fetching agrofy dolar blue values from cache or site."""
    source_name = "agrofy"

    @staticmethod
    def get_blue() -> Optional[DolarBlue]:
        """Fetch the agrofy values from agrofy as DolarBlue."""

        try:
            return scrape_dolar_values_from_source(
                "agrofy",
                agrofy_selenium_fetching,
                agrofy_soup_scraping
            )

        except ScrapingException as scep:
            logging.error(scep)
            logging.error("Error fetching dolarhoy dolar blue value")
            return None
