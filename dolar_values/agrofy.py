"""Fetching the values from agrofy."""
from classes.dolar_blue import DolarBlue
from libs.scraping.agrofy.utils import agrofy_soup_scraping, agrofy_selenium_fetching
from libs.scraping.scrape_page import get_dolar_values_from_source

def get_agrofy_values() -> DolarBlue:
    """Fetch the dolarblue values from agrofy as DolarBlue."""

    return get_dolar_values_from_source(
        "agrofy",
        agrofy_selenium_fetching,
        agrofy_soup_scraping
    )
