# pylint: disable=wrong-import-position
# pylint: disable=unused-import

"""Python backend flask API for dolarblue prices in Argentina,
obtained by webscraping different sites, and requesting prices via different apis"""

__author__ = "Gaston Otero"
__version__ = "0.0 Alpha"
__maintainer__ = "Gaston Otero"
__email__ = "mail@gastonotero.com"

# Initialize environment
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initailize flask & routes
from flask import Flask

logging.info("Starting Flask server.")
app = Flask(__name__)

import src.public_interfaces.flask_routes.get_all

# Initialize telegram bot
from src.public_interfaces.telegram_bot.start_bot import start_telegram_bot

logging.info("Starting Telegram bot.")
start_telegram_bot()

# Initialize main "update-dolarblue-values" subscriber
from src.pub_sub.main_dolarblue_updater import dolarblue_update_request_handler

logging.info("Starting main dolarblue update request handler.")
dolarblue_update_request_handler()
