"""Route for handling and sending all the possible data"""

import json
from typing import Any, Dict

from flask.wrappers import Response
from main import app
from classes import DolarBlueSource

@app.get("/get_all")
def get_all_route() -> Response:
    """Route for fetching the cached data for all the sources."""

    all_values: Dict[str, Dict[str, Any]] = {}

    for src in DolarBlueSource.get_all():
        value = src.get_cached_blue()
        if value:
            all_values[src.source_name] = value.to_dict()

    response = app.response_class(
        response=json.dumps(all_values),
        status=200,
        mimetype='application/json'
    )

    return response

@app.get("/update")
def update_cache() -> str:
    """TESTING"""

    for src in DolarBlueSource.get_all():
        src.update_cache()

    return "done"
