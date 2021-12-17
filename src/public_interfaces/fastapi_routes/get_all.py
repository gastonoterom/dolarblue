from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from src.classes import DolarBlueUtils

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

    return DolarBlueUtils.get_all_dolarblue_dict()


@router.get("/update")
async def update_route() -> Dict[str, str]:
    """Route for fetching the cached data for all the sources."""

    DolarBlueUtils.request_cache_update()

    return {"response": "Updating dolarblue values"}
