"""Fetching the values from agrofy."""

from classes.dolar_blue import DolarBlue
from libs.scraping.dolarhoy.utils import dolarhoy_selenium_fetching, dolarhoy_soup_scraping
from libs.scraping.scrape_page import get_dolar_values_from_source

def get_dolarhoy_values() -> DolarBlue:
    """Fetch the dolarblue values from dolarhoy as DolarBlue."""

    return get_dolar_values_from_source(
        "dolarhoy",
        dolarhoy_selenium_fetching,
        dolarhoy_soup_scraping
    )
