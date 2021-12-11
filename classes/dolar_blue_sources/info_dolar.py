"""Module that fetches Infodolar dolar blue values from cache or site."""

from classes.scraping_source import ScrapingSource
from libs.scraping.infodolar.utils import infodolar_selenium_fetching, infodolar_soup_scraping

class InfoDolar(ScrapingSource):
    """Class for fetching Infodolar dolar blue values from cache or site."""

    source_name = "infodolar"
    selenium_fetching = infodolar_selenium_fetching
    soup_scraping = infodolar_soup_scraping
