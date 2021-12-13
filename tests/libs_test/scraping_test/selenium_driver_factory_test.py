# pylint: disable=missing-docstring

import unittest
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory

class TestSeleniumDriverFactory(unittest.TestCase):

    def test_local_driver(self) -> None:

        driver = SeleniumDriverFactory.get_driver()

        driver.close()
        driver.quit()

    def test_remote_driver(self) -> None:

        driver = SeleniumDriverFactory.get_driver()

        driver.close()
        driver.quit()
