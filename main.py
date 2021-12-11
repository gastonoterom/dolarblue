"""Python backend flask API for dolarblue prices in Argentina,
obtained by webscraping different sites, and requesting prices via different apis"""

__author__ = "Gaston Otero"
__version__ = "0.0 Alpha"
__maintainer__ = "Gaston Otero"
__email__ = "mail@gastonotero.com"


from dolar_values.agrofy import get_agrofy_values
from dolar_values.dolarhoy import get_dolarhoy_values

def main() -> None:
    """Starting the server and initializing config variables"""

    # Fetching agrofy dolar values
    agrofy_dolar_blue = get_agrofy_values()
    # Fetching dolarhoy dolar values
    dolarhoy_dolar_blue = get_dolarhoy_values()

    print(agrofy_dolar_blue, dolarhoy_dolar_blue)
    
    return


if __name__ == "__main__":
    main()
