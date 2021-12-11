"""List with all the working dolarblue sources"""

from typing import List
from classes.dolar_blue_source import DolarBlueSource
from classes.dolar_blue_sources.agrofy import Agrofy
from classes.dolar_blue_sources.dolar_hoy import DolarHoy
from classes.dolar_blue_sources.info_dolar import InfoDolar

all_dolar_blue_sources: List[DolarBlueSource] = [
    Agrofy(),
    DolarHoy(),
    InfoDolar()
]
