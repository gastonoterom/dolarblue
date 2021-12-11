"""Dolar blue scraper for the site dolarhoy.com"""

from typing import List, Tuple
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from consts.dolarhoy import DOLARHOY_URL

def dolarhoy_soup_scraping(soup: BeautifulSoup) -> Tuple[float, float]:
    """Beautiful soup scraping for dolarhoy dolar blue values,
    returns a touple with the values, the first
    one is the BUY value, the second the SELL value"""

    try:
        prices: List[float] = []

        for divs in soup.find_all("div", class_="value"):
            prices.append(float(divs.text.replace("$","")))

        return prices[0], prices[1]

    except ValueError as v_e:
        raise Exception("Error parsing dolarhoy page") from v_e

def dolarhoy_selenium_fetching(driver: WebDriver) -> str:
    """Returns the content of the dolarhoy
    page with the value of the dolar blue already loaded."""

    try:
        driver.get(DOLARHOY_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cotizacion_value"))
        )
        content = driver.page_source
        return content

    except Exception as err:
        raise Exception("Error fetching dolarhoy page") from err
