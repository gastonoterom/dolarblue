"""Selenium utils module"""
from typing import Any, Callable, Optional
import inspect
from selenium.webdriver.remote.webdriver import WebDriver
from libs.scraping.config import REMOTE_SELENIUM_URL
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory

class MethodNotCompatibleError(Exception):
    """Exception for incompatible decorated methods"""
class NonSeleniumDriverException(Exception):
    """Exception when the function is called with a NON selenium driver."""

def selenium_injection( selenium_requirer: Callable ):
    """Selenium driver injector for method that requires it as driver kwarg.
    Decorated function MUST have a 'driver: Optional[WebDriver]' argument!"""
    inspected_requirer = inspect.getfullargspec(selenium_requirer)

    def inject_driver(*args, **kwargs) -> Optional[Any]:
        """Inject the driver into the selenium_requirer function"""

        # Check that the injected function accepts "driver: Optional[WebDriver]" as an argument
        if "driver" not in inspected_requirer.args or \
          Optional[WebDriver] != inspected_requirer.annotations.get("driver"):

            raise MethodNotCompatibleError("Decorated function is incompatible:\
            it has no 'driver: Optional[WebDriver]' argument")

        # If the function already had a "driver" sent when called, check it is a selenium driver
        if kwargs.get("driver") and not isinstance(kwargs.get("driver"), WebDriver):

            raise NonSeleniumDriverException("Error in selenium injection: previous \
            driver passed is not a selenium driver")

        # If the function was called without a driver provided, create one and inject it
        if kwargs.get("driver") is None:
            driver = SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL)
            kwargs["driver"] = driver

        # If the function throws an exception, the handling responsability is from the caller,
        # We just make sure the driver is properly closed (could be done with a context manager).
        try:
            # Execute the original function
            response = selenium_requirer(*args, **kwargs)

        finally:
            # Close the driver (if created)
            if driver:
                driver.close()
                driver.quit()

        return response

    return inject_driver
