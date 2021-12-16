from typing import Any, Dict
from fastapi import APIRouter
from src.classes import DolarBlueSource

router = APIRouter()


@router.get("/get_all")
async def get_all_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the sources."""

    all_values: Dict[str, Dict[str, Any]] = {}
    for src in DolarBlueSource.get_all():
        value = src.get_cached_blue()
        if value:
            all_values[src.source_name] = value.to_dict()

    return all_values
