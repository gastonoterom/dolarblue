import logging
from typing import Dict, Optional
from src.classes import DolarBlueUtils
from src.classes.dolar_blue import DolarBlue, DolarBlueSource
from src.pub_sub.subscribers.update_values_sub import subscribe_to_update_request, \
    subscribe_to_cache_updated
from src.pub_sub.publishers.update_values_pub import pub_values_updated


@subscribe_to_update_request
def handle_dolarblue_update_request() -> None:
    """This function updates in cache all the dolarblue sources."""

    logging.info("Updating dolar blue values.")

    updated_sources = DolarBlueUtils.update_all()
    pub_values_updated(updated_sources)


@subscribe_to_cache_updated
def handle_cache_updated(report: Dict[str, Optional[DolarBlue]]) -> None:
    """This function gets the report from all the sources updated and creates an average report
    from all the sources that were successfully fetched"""

    logging.info("Creating average dolarblue value")

    buy = sell = 0.0
    for val in report.values():
        if val is None:
            continue
        buy += val.buy_price
        sell += val.sell_price

    buy = round(buy / len(report.values()), 2)
    sell = round(sell / len(report.values()), 2)

    average_source = DolarBlueSource("average", lambda: (buy, sell))
    average_source.update_cache()
