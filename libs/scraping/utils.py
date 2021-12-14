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

def check_driver_in_arguments(function_to_inspect: Callable) -> None:
    """Checks if the function to inspect has a 'driver: Optional[WebDriver]' argument.
    Raises Exception if not."""
    function_inspection = inspect.getfullargspec(function_to_inspect)
    try:
        assert "driver" in function_inspection.args
        assert Optional[WebDriver] == function_inspection.annotations.get("driver")

    except AssertionError as assert_err:
        raise MethodNotCompatibleError("Decorated function is incompatible:\
            it has no 'driver: Optional[WebDriver]' argument") from assert_err

def check_valid_driver(kwarg_driver: Any) -> None:
    """Checks if the input is a valid WebDriver instance, raises Exception if not."""
    try:
        assert isinstance(kwarg_driver, WebDriver)

    except AssertionError as assert_err:
        raise NonSeleniumDriverException("Error in selenium injection: previous \
            driver passed is not a selenium driver") from assert_err

def selenium_injection( selenium_requirer: Callable ):
    """Selenium driver injector for method that requires it as driver kwarg.
    Decorated function MUST have a 'driver: Optional[WebDriver]' argument!"""

    def inject_driver(*args, **kwargs) -> Optional[Any]:
        """Inject the driver into the selenium_requirer function"""

        # Check that the injected function accepts "driver: Optional[WebDriver]" as an argument
        check_driver_in_arguments(selenium_requirer)

        # If the function already had a "driver" sent when called, check it is a selenium driver
        if kwarg_driver := kwargs.get("driver"):
            check_valid_driver(kwarg_driver)

        # If the function was called without a driver provided, create one and inject it
        else:
            driver = SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL)
            kwargs["driver"] = driver

        response = selenium_requirer(*args, **kwargs)

        if driver:
            driver.close()
            driver.quit()

        return response

    return inject_driver
