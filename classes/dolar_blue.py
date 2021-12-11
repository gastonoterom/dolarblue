"""Dolarblue class representing the selling and buying price from itself."""
from dataclasses import dataclass

@dataclass
class DolarBlue():
    """Dolarblue class: links a source to a buying and selling price."""
    source: str
    buy_price: float
    sell_price: float
