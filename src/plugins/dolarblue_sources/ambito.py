from typing import Callable, Tuple
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.libs.scraping.scrape_page import scrape_dolar_values_from_source

AMBITO_URL = "https://www.ambito.com/contenidos/dolar-informal.html"


def ambito_soup_scraping(soup: BeautifulSoup) -> Tuple[float, float]:
    """Beautiful soup scraping for ambito dolar blue values,
    returns a touple with the values, the first
    one is the BUY value, the second the SELL value"""
    try:

        buy_price_soup = soup.find("span", class_="data-compra")
        sell_price_soup = soup.find("span", class_="data-venta")

        assert buy_price_soup is not None and sell_price_soup is not None

        buy_price = float(buy_price_soup.text.replace(",", "."))
        sell_price = float(sell_price_soup.text.replace(",", "."))

        return buy_price, sell_price

    except ValueError as v_e:
        raise Exception("Error parsing ambito page:") from v_e


def ambito_selenium_fetching(driver: WebDriver) -> str:
    """Returns the content of the ambito
    page with the value of the dolar blue already loaded."""

    try:
        driver.get(AMBITO_URL)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (
                    By.CLASS_NAME,
                    "data-compra"
                ),
                ",")
        )
        content = driver.page_source
        return content

    except Exception as err:
        raise Exception("Error fetching ambito page") from err


def scrape_ambito_values() -> Tuple[float, float]:
    """Scraping function for ambito"""

    return scrape_dolar_values_from_source(
        ambito_selenium_fetching,
        ambito_soup_scraping,
    )


def get_plugin() -> Tuple[str, Callable[[], Tuple[float, float]]]:
    """Returns the plugins name & fetching strategy"""
    return (
        "ambito",
        scrape_ambito_values
    )
