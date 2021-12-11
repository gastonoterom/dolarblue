"""Route for handling and sending all the possible data"""

from typing import Any, Dict
from main import app
from classes.dolar_blue_sources.all_sources import all_dolar_blue_sources

@app.route("/update")
def update_route() -> str:
    for src in all_dolar_blue_sources:
        src.update_cache()

    return "done"

@app.route("/")
def root_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the sources."""

    all_values: Dict[str, Dict[str, Any]] = {}

    for src in all_dolar_blue_sources:
        value = src.get_cached_blue()
        if value:
            all_values[src.source_name] = value.to_dict()

    return all_values
