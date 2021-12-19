from typing import Callable, List,  Tuple
from urllib import request
from bs4 import BeautifulSoup

LANACION_URL = "https://www.lanacion.com.ar/dolar-hoy/"


def lanacion_soup_scraping(soup: BeautifulSoup) -> Tuple[float, float]:
    """Beautiful soup scraping for lanacion dolar blue values,
    returns a touple with the values, the first
    one is the BUY value, the second the SELL value"""

    try:
        prices: List[float] = []

        dolarblue_div = soup.find_all("div", class_="currency-data")[1]

        for strong in dolarblue_div.find_all("strong", class_="--fourxs"):
            prices.append(
                float(strong.text.replace("$", "").replace(",", "."))
            )

        return prices[0], prices[1]

    except ValueError as v_e:
        raise Exception("Error parsing lanacion page:") from v_e


def scrape_lanacion_values() -> Tuple[float, float]:
    """Scraping function for lanacion"""
    page = request.urlopen(LANACION_URL)

    return lanacion_soup_scraping(
        BeautifulSoup(page, features="html.parser")
    )


def get_plugin() -> Tuple[str, Callable[[], Tuple[float, float]]]:
    """Returns the plugins name & fetching strategy"""
    return (
        "lanacion",
        scrape_lanacion_values
    )
