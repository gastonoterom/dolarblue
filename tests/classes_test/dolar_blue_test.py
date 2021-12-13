# pylint: disable=missing-docstring

import unittest
from datetime import datetime
from classes.dolar_blue import DolarBlue

class TestDolarBlue(unittest.TestCase):

    def test_dolarblue(self) -> None:

        date_now = datetime.now().timestamp()
        dolar_blue = DolarBlue("agrofy", 99.5, 200.5)

        self.assertEqual(dolar_blue.source, "agrofy")
        self.assertEqual(dolar_blue.buy_price, 99.5)
        self.assertEqual(dolar_blue.sell_price, 200.5)
        self.assertEqual(dolar_blue.average, 150)
        self.assertTrue(abs(dolar_blue.date_time.timestamp() - date_now) <= 10)

        dolar_blue_dict = dolar_blue.to_dict()

        dolar_blue_dict_test = {
            "buy_price": 99.5,
            "sell_price": 200.5,
            "average_price": 150,
            "date_time": dolar_blue.date_time
        }

        for key, key_test in zip(
            dolar_blue_dict,
            dolar_blue_dict_test
        ):
            self.assertEqual(key, key_test)

        for val, val_test in zip(
            dolar_blue_dict,
            dolar_blue_dict_test
        ):
            self.assertEqual(val, val_test)
