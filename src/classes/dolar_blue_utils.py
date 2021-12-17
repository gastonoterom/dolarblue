from __future__ import annotations
from typing import Any, Dict, List
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from src.classes.dolar_blue import DolarBlue
from src.classes.dolar_blue_source import DolarBlueSource
from src.libs.scraping.dolar_blue_sources.agrofy.utils import scrape_agrofy_values
from src.libs.scraping.dolar_blue_sources.dolarhoy.utils import scrape_dolarhoy_values
from src.libs.scraping.dolar_blue_sources.infodolar.utils import scrape_infodolar_values
from src.pub_sub.publishers.update_values_pub import pub_update_values


class DolarBlueUtils:
    """Class for dolarblue utilities, like getting all the DolarBlueSources or updating
    all the DolarBlueSources"""

    @staticmethod
    def get_all() -> List[DolarBlueSource]:
        """Gets all the existent dolar blue sources."""
        return [
            DolarBlueSource(source_name="agrofy",
                            fetching_function=scrape_agrofy_values),
            DolarBlueSource(source_name="infodolar",
                            fetching_function=scrape_infodolar_values),
            DolarBlueSource(source_name="dolarhoy",
                            fetching_function=scrape_dolarhoy_values,),
        ]

    @staticmethod
    def update_all() -> Dict[str, bool]:
        """Updates all the DolarBlue values in the cache store,
        returns a report of each source names and their respective valid update or failure."""

        async def update_all_async() -> Dict[str, bool]:
            """This runs each update_cache in a different thread in an async fashion, to it is
            much faster than running each one by itself"""
            loop = asyncio.get_running_loop()
            all_sources = DolarBlueUtils.get_all()
            executor = ThreadPoolExecutor(len(all_sources))
            jobs = []

            for src in all_sources:
                jobs.append(loop.run_in_executor(executor, src.update_cache))

            jobs_report = await asyncio.gather(*jobs)

            return {src.source_name: rsp for src, rsp in zip(all_sources, jobs_report)}

        return asyncio.run(update_all_async())

    @staticmethod
    def get_all_dolarblue_values() -> List[DolarBlue]:
        """Gets all the known cached dolarblue values for each source of information."""
        return list(
            filter(
                None,
                [src.get_cached_blue() for src in DolarBlueUtils.get_all()]
            )
        )

    @staticmethod
    def get_all_dolarblue_dict() -> Dict[str, Dict[str, Any]]:
        """Gets all the cached dolarblue values for each source of information in a JSON
        serializable dictionary."""

        return {
            dolarblue.source: dolarblue.to_dict()
            for dolarblue in DolarBlueUtils.get_all_dolarblue_values()
        }

    @staticmethod
    def request_cache_update():
        """Publish a cache update request message to the pubsub manager

        This method should be called when a request from the admin or the job manager
        to update the cache is needed."""
        pub_update_values()
