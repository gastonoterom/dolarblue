"""Selenium utils module"""
from typing import Any, Callable, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from libs.scraping.config import REMOTE_SELENIUM_URL
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory


def selenium_injection(
        selenium_requirer: Callable[
            [
                Any,
                Optional[WebDriver]
            ],
            Optional[Any]]
        ):
    """Selenium driver injector for instance method that requires it."""

    def inject_driver(self, driver: Optional[WebDriver] = None) -> Optional[Any]:
        if driver is None:
            driver = SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL)
        response = selenium_requirer(self, driver)
        if driver:
            driver.close()
            driver.quit()
        return response

    return inject_driver
