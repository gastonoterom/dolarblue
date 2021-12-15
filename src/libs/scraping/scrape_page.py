"""Module for web scraping different sources to get the DolarBlue data"""

from typing import Callable, Tuple
from bs4 import BeautifulSoup

from selenium.webdriver.remote.webdriver import WebDriver
from src.libs.custom_exceptions.fetching_exception import FetchingException
from src.libs.scraping.utils import selenium_provided


@selenium_provided
def scrape_dolar_values_from_source(
    # Selenium function that returns the html with the dolar blue prices present
    selenium_fetching: Callable[[WebDriver], str],
    # Soup function that returns a tuple with the buy/sell price
    soup_scraping: Callable[[BeautifulSoup], Tuple[float, float]],
    # Selenium driver (provided by the decorator if sent None)
    driver: WebDriver
) -> Tuple[float, float]:
    """Function for getting the dolar blue buy & sell value of a certain source,
    using the proper selenium_fetching and soup_scraping functions.
    If no driver sent one will be provided by the @selenium_provided."""

    try:
        content = selenium_fetching(driver)
        return soup_scraping(BeautifulSoup(content, features="html.parser"))

    except Exception as err:
        raise FetchingException("Error getting USD values") from err
