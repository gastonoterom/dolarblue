import logging
from src.pub_sub.subscribers.update_values_sub import subscribe_to_update_request
from src.classes import DolarBlueSource
from src.pub_sub.publishers.update_values_pub import pub_values_updated


@subscribe_to_update_request
def handle_dolarblue_update_request():
    logging.info("Updating dolar blue values.")

    updated_sources = DolarBlueSource.update_all()
    pub_values_updated(updated_sources)
