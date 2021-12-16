

class FetchingException(Exception):
    """Raised when a scraping, xml or rest api fetching fails"""


class MethodNotCompatibleError(Exception):
    """Exception for methods decorated that don't support the 'driver: WebDriver' argument"""


class NonSeleniumDriverException(Exception):
    """Exception when the function is called with a NON selenium driver as a driver kwarg."""
