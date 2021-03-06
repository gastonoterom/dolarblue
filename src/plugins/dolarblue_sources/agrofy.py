from typing import Callable, List, Tuple
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.libs.scraping.scrape_page import scrape_dolar_values_from_source

AGROFY_URL = "https://news.agrofy.com.ar/economia-politica/dolar"


def agrofy_soup_scraping(soup: BeautifulSoup) -> Tuple[float, float]:
    """Beautiful soup scraping for agrofy dolar blue values,
    returns a touple with the values, the first
    one is the BUY value, the second the SELL value"""

    try:
        wanted_row = None
        title_col: int
        prices: List[float] = []

        for row_i, row in enumerate(soup.find_all("tr", class_="odd-item")):
            for col_i, col in enumerate(row.find_all("td")):
                if col.text == "U$ Blue":
                    wanted_row = row_i
                    title_col = col_i
                    continue

                if row_i == wanted_row and col_i-title_col <= 2:
                    prices.append(float(col.text.replace(",", ".")))

            if wanted_row:
                break

        return prices[0], prices[1]

    except ValueError as v_e:
        raise Exception("Error parsing agrofy page:") from v_e


def agrofy_selenium_fetching(driver: WebDriver) -> str:
    """Returns the content of the agrofy
    page with the value of the dolar blue already loaded."""

    try:
        driver.get(AGROFY_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-agrofy"))
        )
        content: str = driver.page_source
        return content

    except Exception as err:
        raise Exception("Error fetching agrofy page") from err


def scrape_agrofy_values() -> Tuple[float, float]:
    """Scraping function for agrofy"""

    return scrape_dolar_values_from_source(
        agrofy_selenium_fetching,
        agrofy_soup_scraping,
    )


def get_plugin() -> Tuple[str, Callable[[], Tuple[float, float]]]:
    """Returns the plugins name & fetching strategy"""
    return (
        "agrofy",
        scrape_agrofy_values
    )
