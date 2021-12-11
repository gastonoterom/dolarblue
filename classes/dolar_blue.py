"""Dolarblue class representing the selling and buying price from itself."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DolarBlue():
    """Dolarblue class: links a source to a buying and selling price."""
    source: str
    buy_price: float
    sell_price: float
    date_time: datetime = datetime.now()

    @property
    def average(self) -> float:
        """Calculate the average between the sell and buy price"""
        return (self.buy_price + self.sell_price) / 2
