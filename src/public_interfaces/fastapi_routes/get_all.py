from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from src.classes import DolarBlueSource

router = APIRouter()


class ResponseBodySchema(BaseModel):
    """Example schema for the response documentation of the get_all route"""
    buy_price: float = 210
    sell_price: float = 211
    average_price: float = 210.50
    date_time: str = "12-15-2021 19:18:22"


@router.get("/get_all", response_model=Dict[str, ResponseBodySchema])
async def get_all_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the sources."""

    all_values: Dict[str, Dict[str, Any]] = {}
    for src in DolarBlueSource.get_all():
        value = src.get_cached_blue()
        if value:
            all_values[src.source_name] = value.to_dict()

    return all_values
