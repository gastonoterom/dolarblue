# pylint: disable=wrong-import-position
"""Python backend flask API for dolarblue prices in Argentina,
obtained by webscraping different sites, and requesting prices via different apis"""

__author__ = "Gaston Otero"
__version__ = "0.0 Alpha"
__maintainer__ = "Gaston Otero"
__email__ = "mail@gastonotero.com"

# Initialize environment
from dotenv import load_dotenv # pylint: disable=wrong-import-order
load_dotenv()
# Initailize flask
from flask import Flask  # pylint: disable=wrong-import-order
app = Flask(__name__)


import logging # pylint: disable=wrong-import-order
from routes import all_sources # pylint: disable=unused-import

def main() -> None:
    """Starting the server and initializing config variables"""
    logging.basicConfig()

if __name__ == "__main__":
    main()
