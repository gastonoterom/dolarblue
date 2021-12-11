"""Module for web scraping different sources to get the DolarBlue data"""

from typing import Callable, Tuple
from bs4 import BeautifulSoup

from selenium.webdriver.remote.webdriver import WebDriver
from classes.dolar_blue import DolarBlue
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory
from consts.selenium_values import REMOTE_SELENIUM_URL

def get_dolar_values_from_source(
    page_name: str,
    selenium_fetching: Callable[[WebDriver], str],
    soup_scraping: Callable[[BeautifulSoup], Tuple[float, float]]
    ) -> DolarBlue:
    """Function for getting the dolar blue value of a certain source, using the page
    source name, and the specific selenium fetching and soup scraping functions for said
    source."""

    try:
        driver = SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL)

    except Exception as err:
        raise Exception("Error getting selenium driver") from err

    try:
        content = selenium_fetching(driver)
        buy_value, sell_value =  soup_scraping(BeautifulSoup(content, features="html.parser"))

        return DolarBlue(source=page_name, buy_price=buy_value, sell_price=sell_value)

    except Exception as err:
        raise Exception(f"Error getting {page_name} USD values") from err

    finally:
        driver.close()
        driver.quit()
