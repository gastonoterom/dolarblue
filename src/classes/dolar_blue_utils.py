from __future__ import annotations
from typing import Any, Dict, List, Optional
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from src.classes.dolar_blue import DolarBlue, DolarBlueSource
from src.libs.utils import log_runtime
from src.pub_sub.publishers.update_values_pub import pub_update_values
from src.plugins import get_plugins


class DolarBlueUtils:
    """Class for dolarblue utilities, like getting all the DolarBlueSources or updating
    all the DolarBlueSources"""

    @staticmethod
    def get_average() -> DolarBlueSource:
        """Gets the average buy/sell price from all the scraped sources"""
        return DolarBlueSource("average")

    @staticmethod
    def get_all() -> List[DolarBlueSource]:
        """Gets all the existent dolar blue sources from the plugins."""

        return [
            DolarBlueSource(plugin[0], plugin[1])
            for plugin in get_plugins()
        ]

    @staticmethod
    @log_runtime
    def update_all() -> Dict[str, Optional[DolarBlue]]:
        """Updates all the DolarBlue values in the cache store,
        returns a report of each source names and their respective valid update or failure.

        The key of the dictionary is the name of the dolarblue source and the object is a dolarblue
        object in case the update was successful. Otherwise, the value of that key is None."""

        async def update_all_async() -> Dict[str, Optional[DolarBlue]]:
            """This runs each update_cache in a different thread in an async fashion, to it is
            much faster than running each one by itself"""
            with ThreadPoolExecutor() as pool:

                loop = asyncio.get_running_loop()
                all_sources = DolarBlueUtils.get_all()

                jobs_report = await asyncio.gather(
                    *[
                        loop.run_in_executor(pool, src.update_cache)
                        for src in all_sources
                    ]
                )

                return {src.source_name: dolar for src, dolar in zip(all_sources, jobs_report)}

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
            dolarblue.source.source_name: dolarblue.to_dict()
            for dolarblue in DolarBlueUtils.get_all_dolarblue_values()
        }

    @staticmethod
    def request_cache_update():
        """Publish a cache update request message to the pubsub manager

        This method should be called when a request from the admin or the job manager
        to update the cache is needed."""
        pub_update_values()
