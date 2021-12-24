# pylint: disable=wrong-import-order,wrong-import-position,ungrouped-imports

"""Python backend flask API for dolarblue prices in Argentina,
obtained by webscraping different sites, and requesting prices via different apis"""

__author__ = "Gaston Otero"
__version__ = "0.0 Alpha"
__maintainer__ = "Gaston Otero"
__email__ = "mail@gastonotero.com"

# Setup the environment
from dotenv import load_dotenv

load_dotenv()


# Initialize Logging
import logging

logging.basicConfig(level=logging.INFO)

# Initialize plugins
from src.plugins import load_plugins

logging.info("Loading plugins")
load_plugins()

# Initialize fastapi & routes
from fastapi import FastAPI
from src.public_interfaces.fastapi_routes.get_all import router as get_all_router


logging.info("Starting Fastapi server")
app = FastAPI()
app.include_router(get_all_router)

# Initialize telegram bot
from src.public_interfaces.telegram_bot.start_bot import start_telegram_bot

logging.info("Starting Telegram bot.")
start_telegram_bot()

# Initialize main "update-dolarblue-values" subscriber
from src.pub_sub.main_dolarblue_updater import handle_dolarblue_update_request, handle_cache_updated

logging.info("Starting main dolarblue update request handler.")
handle_dolarblue_update_request()
handle_cache_updated()

# Start all the scheduled jobs
from src.jobs.start_jobs import start_all_jobs

logging.info("Setting up the scheduler")
start_all_jobs()
