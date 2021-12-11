"""Route for handling and sending all the possible data"""

from typing import Any, Dict
from main import app
from classes.agrofy import Agrofy
from classes.dolar_hoy import DolarHoy

@app.route("/")
def root_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the sources."""

    all_values: Dict[str, Dict[str, Any]] = {}
    for source, value in zip(
        [
            "agrofy",
            "dolarhoy"
        ],
        [
            Agrofy.get_cached_blue(),
            DolarHoy.get_cached_blue()
        ]):
        if value:
            all_values[source] = value.to_dict()

    return all_values

@app.route("/prev")
def prev_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the previouse sources."""

    all_values: Dict[str, Dict[str, Any]] = {}
    for source, value in zip(
        [
            "agrofy",
            "dolarhoy"
        ],
        [
            Agrofy.get_prev_cached_blue(),
            DolarHoy.get_prev_cached_blue()
        ]):
        if value:
            all_values[source] = value.to_dict()

    return all_values
