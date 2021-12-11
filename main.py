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

import logging # pylint: disable=wrong-import-order
from classes.agrofy import Agrofy
from classes.dolar_hoy import DolarHoy

def main() -> None:
    """Starting the server and initializing config variables"""
    logging.basicConfig()

    # Fetching agrofy dolar values
    Agrofy.update_cache()
    # Fetching dolarhoy dolar values
    DolarHoy.update_cache()

    # Displaying cached values
    print(Agrofy.get_cached_blue())
    print(DolarHoy.get_cached_blue())
    print(Agrofy.get_prev_cached_blue())
    print(DolarHoy.get_prev_cached_blue())


if __name__ == "__main__":
    main()
