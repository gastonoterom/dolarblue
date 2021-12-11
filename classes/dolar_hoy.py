"""Module that fetches DolarHoy dolar blue values from cache or site."""
import logging
from typing import Optional
from classes.dolar_blue import DolarBlue
from classes.dolar_blue_source import DolarBlueSource
from libs.scraping.dolarhoy.utils import dolarhoy_selenium_fetching, dolarhoy_soup_scraping
from libs.scraping.exceptions.scraping_error import ScrapingException
from libs.scraping.scrape_page import scrape_dolar_values_from_source


class DolarHoy(DolarBlueSource):
    """Class for fetching DolarHoy dolar blue values from cache or site."""
    source_name = "dolarhoy"

    @staticmethod
    def get_blue() -> Optional[DolarBlue]:
        """Fetch the dolarblue values from dolarhoy as DolarBlue."""

        try:
            return scrape_dolar_values_from_source(
                "dolarhoy",
                dolarhoy_selenium_fetching,
                dolarhoy_soup_scraping
            )

        except ScrapingException as scep:
            logging.error(scep)
            logging.error("Error fetching dolarhoy dolar blue value")
            return None
