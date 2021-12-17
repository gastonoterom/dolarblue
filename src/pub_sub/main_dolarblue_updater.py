import logging
from src.classes import DolarBlueUtils
from src.pub_sub.subscribers.update_values_sub import subscribe_to_update_request
from src.pub_sub.publishers.update_values_pub import pub_values_updated


@subscribe_to_update_request
def handle_dolarblue_update_request():
    """This function updates in cache all the dolarblue sources."""

    logging.info("Updating dolar blue values.")

    updated_sources = DolarBlueUtils.update_all()
    pub_values_updated(updated_sources)
