"""Route for handling and sending all the possible data"""

from main import app
from classes.agrofy import Agrofy
from classes.dolar_hoy import DolarHoy

@app.route("/all_sources")
def all_sources():
    """Route for fetching the cached data for all the sources."""

    all_values = {
        "agrofy": Agrofy.get_cached_blue().to_dict(),
        "dolarhoy": DolarHoy.get_cached_blue().to_dict()
    }

    return all_values

@app.route("/all_prev_sources")
def all_prev_sources():
    """Route for fetching the cached data for all the previouse sources."""

    all_values = {
        "agrofy": Agrofy.get_prev_cached_blue().to_dict(),
        "dolarhoy": DolarHoy.get_prev_cached_blue().to_dict()
    }

    return all_values
