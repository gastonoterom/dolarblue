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

# Initailize flask
from flask import Flask
from flask.logging import create_logger

app = Flask(__name__)

logging.info("Starting Flask server.")

# Import routes
from public_interfaces.flask_routes import get_all

# Initialize telegram bot
from public_interfaces.telegram_bot.start_telegram_bot import start_telegram_bot
start_telegram_bot()
