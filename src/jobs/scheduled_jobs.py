import logging
from src.classes import DolarBlueUtils


def send_dolarblue_update_request():
    """This function publishes an update request petition to the pubsub manager, it can be called
    periodically to always have the latest dolarblue values in cache"""

    logging.info("Running 'send dolarblue update request' job")

    DolarBlueUtils.request_cache_update()
