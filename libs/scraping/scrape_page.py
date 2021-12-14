"""Module for web scraping different sources to get the DolarBlue data"""

from typing import Callable, Tuple
from bs4 import BeautifulSoup

from selenium.webdriver.remote.webdriver import WebDriver
from libs.scraping.exceptions.scraping_error import ScrapingException

def scrape_dolar_values_from_source(
    # Selenium function that returns the html with the dolar blue prices present
    selenium_fetching: Callable[[WebDriver], str],
    # Soup function that returns a tuple with the buy/sell price
    soup_scraping: Callable[[BeautifulSoup], Tuple[float, float]],
    # Selenium driver
    driver: WebDriver
    ) -> Tuple[float, float]:
    """Function for getting the dolar blue buy & sell value of a certain source,
    using the proper selenium_fetching and soup_scraping functions."""

    try:
        content = selenium_fetching(driver)
        return  soup_scraping(BeautifulSoup(content, features="html.parser"))

    except Exception as err:
        raise ScrapingException("Error getting USD values") from err
