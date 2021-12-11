"""Dolarblue class representing the selling and buying price from itself."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

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

    def to_dict(self) -> Dict[str, Any]:
        """Returns the dolarblue object as a JSON serializable dictionary."""

        return {
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "average_price": self.average,
            "date_time": self.date_time.strftime("%m-%d-%Y %H:%M:%S")
        }
