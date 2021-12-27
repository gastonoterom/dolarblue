import inspect
from functools import wraps
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from src.libs.custom_exceptions.fetching_exception \
    import MethodNotCompatibleError, NonSeleniumDriverException
from src.libs.scraping.config import REMOTE_SELENIUM_URL
from src.libs.scraping.selenium_driver_factory import SeleniumDriverFactory


def selenium_provided(selenium_requirer):
    """This function as a decorator sends as an arg and closes a selenium driver to a function
    that accepts it. Decorated function MUST have a 'driver: WebDriver' argument!

    Raises MethodNotCompatibleError if the decorated method is invalid or NonSeleniumDriverException
    if the selenium driver provided is invalid."""

    # Check that the injected function accepts "driver: WebDriver" as an argument
    inspected_requirer = inspect.getfullargspec(selenium_requirer)

    if "driver" not in inspected_requirer.args or \
            WebDriver != inspected_requirer.annotations.get("driver"):

        raise MethodNotCompatibleError("Decorated function is incompatible: \
            it has no 'driver: WebDriver' argument")

    @wraps(selenium_requirer)
    def provide_driver(*args, **kwargs):

        # If the function already had a "driver" sent when called, check it is a selenium driver
        if kwargs.get("driver") and not isinstance(kwargs.get("driver"), WebDriver):
            raise NonSeleniumDriverException("Error in selenium injection: previous \
                driver passed is not a selenium driver")

        # If the function was called without a driver provided, create one and inject it
        if kwargs.get("driver") is None:
            with SeleniumDriverFactory.get_driver(REMOTE_SELENIUM_URL) as driver:

                kwargs["driver"] = driver
                response = selenium_requirer(*args, **kwargs)
        else:
            response = selenium_requirer(*args, **kwargs)

        return response

    return provide_driver
