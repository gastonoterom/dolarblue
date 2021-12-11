"""Module that fetches DolarHoy dolar blue values from cache or site."""
from classes.scraping_source import ScrapingSource
from libs.scraping.dolarhoy.utils import dolarhoy_selenium_fetching, dolarhoy_soup_scraping


class DolarHoy(ScrapingSource):
    """Class for fetching DolarHoy dolar blue values from cache or site."""

    source_name = "dolarhoy"
    selenium_fetching = dolarhoy_selenium_fetching
    soup_scraping = dolarhoy_soup_scraping
