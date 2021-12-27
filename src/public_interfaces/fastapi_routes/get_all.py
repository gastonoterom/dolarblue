from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from src.classes import DolarBlueUtils

router = APIRouter()


class ResponseBodySchema(BaseModel):
    """Example schema for the response documentation of the get and get_all route"""
    buy_price: float = 210
    sell_price: float = 211
    average_price: float = 210.50
    date_time: str = "15-12-2021 19:18:22"


@router.get("/dolarblue", response_model=ResponseBodySchema)
async def get_average() -> Dict[str, Any]:
    """Route for fetching the cached data for all the sources."""
    cached_average = DolarBlueUtils.get_average().get_cached_blue()

    if cached_average is None:
        return {}

    return cached_average.to_dict()


@router.get("/dolarblue/sources", response_model=Dict[str, ResponseBodySchema])
async def get_all_route() -> Dict[str, Dict[str, Any]]:
    """Route for fetching the cached data for all the sources."""

    return DolarBlueUtils.get_all_dolarblue_dict()
