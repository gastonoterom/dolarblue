"""Module that fetches Agrofy dolar blue values from cache or site."""

from classes.scraping_source import ScrapingSource
from libs.scraping.agrofy.utils import agrofy_soup_scraping, agrofy_selenium_fetching

class Agrofy(ScrapingSource):
    """Class for fetching agrofy dolar blue values from cache or site."""

    source_name = "agrofy"
    selenium_fetching = agrofy_selenium_fetching
    soup_scraping = agrofy_soup_scraping
