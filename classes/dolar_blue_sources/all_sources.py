"""List with all the working dolarblue sources"""

from typing import List
from classes.dolar_blue_source import DolarBlueSource
from classes.dolar_blue_sources import DolarScrapingSource

from libs.scraping.dolar_blue_sources.agrofy.utils \
    import agrofy_selenium_fetching, agrofy_soup_scraping

from libs.scraping.dolar_blue_sources.dolarhoy.utils \
    import dolarhoy_selenium_fetching, dolarhoy_soup_scraping

from libs.scraping.dolar_blue_sources.infodolar.utils \
    import infodolar_selenium_fetching, infodolar_soup_scraping

all_dolar_blue_sources: List[DolarBlueSource] = [
    DolarScrapingSource(
        source_name="agrofy",
        selenium_fetching=agrofy_selenium_fetching,
        soup_scraping=agrofy_soup_scraping
    ),
    DolarScrapingSource(
        source_name="dolarhoy",
        selenium_fetching=dolarhoy_selenium_fetching,
        soup_scraping=dolarhoy_soup_scraping
    ),
    DolarScrapingSource(
        source_name="infodolar",
        selenium_fetching=infodolar_selenium_fetching,
        soup_scraping=infodolar_soup_scraping
    ),
]
