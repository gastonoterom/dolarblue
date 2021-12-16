# pylint: disable=wrong-import-order,wrong-import-position

"""Python backend flask API for dolarblue prices in Argentina,
obtained by webscraping different sites, and requesting prices via different apis"""

from dotenv import load_dotenv
load_dotenv()

import logging
from fastapi import FastAPI
from src.public_interfaces.telegram_bot.start_bot import start_telegram_bot
from src.pub_sub.main_dolarblue_updater import handle_dolarblue_update_request
from src.public_interfaces.fastapi_routes.get_all import router as get_all_router

__author__ = "Gaston Otero"
__version__ = "0.0 Alpha"
__maintainer__ = "Gaston Otero"
__email__ = "mail@gastonotero.com"

# Initialize Logging

logging.basicConfig(level=logging.INFO)

# Initailize fastapi & routes

logging.info("Starting Fastapi server")
app = FastAPI()
app.include_router(get_all_router)

# Initialize telegram bot
logging.info("Starting Telegram bot.")
start_telegram_bot()

# Initialize main "update-dolarblue-values" subscriber

logging.info("Starting main dolarblue update request handler.")
handle_dolarblue_update_request()
