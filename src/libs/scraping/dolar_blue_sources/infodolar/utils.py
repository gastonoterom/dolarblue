from typing import List, Tuple
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.libs.scraping.dolar_blue_sources.config import INFODOLAR_URL
from src.libs.scraping.scrape_page import scrape_dolar_values_from_source


def infodolar_soup_scraping(soup: BeautifulSoup) -> Tuple[float, float]:
    """Beautiful soup scraping for infodolar dolar blue values,
    returns a touple with the values, the first
    one is the BUY value, the second the SELL value"""

    try:
        prices: List[float] = []

        for _, row in enumerate(
            soup.find_all("table", id="CompraVenta")[
                0].find_all("td", class_="colCompraVenta")
        ):
            row.find("span").decompose()
            price = row.text.rstrip().replace(" ", "").replace("$", "").replace(",", ".")
            prices.append(float(price))

        return prices[0], prices[1]

    except ValueError as v_e:
        raise Exception("Error parsing infodolar page:") from v_e


def infodolar_selenium_fetching(driver: WebDriver) -> str:
    """Returns the content of the infodolar
    page with the value of the dolar blue already loaded."""

    try:
        driver.get(INFODOLAR_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "colCompraVenta"))
        )
        content = driver.page_source
        return content

    except Exception as err:
        raise Exception("Error fetching infodolar page") from err


def scrape_infodolar_values() -> Tuple[float, float]:
    """Scraping function for infodolar"""

    return scrape_dolar_values_from_source(
        infodolar_selenium_fetching,
        infodolar_soup_scraping
    )
