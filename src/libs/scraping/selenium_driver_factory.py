from typing import Any, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from src.libs.scraping.config import HEADLESS_SELENIUM


class SeleniumDriverFactory():
    """This class has class methods for constructing selenium driver objects."""

    @staticmethod
    def get_default_options() -> Options:
        """Get default options for the selenium driver."""
        options = Options()
        options.headless = HEADLESS_SELENIUM
        options.add_argument("--silent")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_prefs: Dict[str, Any] = {}
        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        return options

    @classmethod
    def get_driver(
        cls,
        remote_url: Optional[str] = None,
        options: Optional[Options] = None
    ) -> WebDriver:
        """Creates and returns a local or remote selenium driver,
        depending if the remote url was given or not,
        if options not given it just returns a driver with default options"""

        if options is None:
            options = cls.get_default_options()

        if remote_url:
            return cls.get_remote_driver(options, remote_url)
        else:
            return cls.get_local_driver(options)

    @staticmethod
    def get_local_driver(options: Options) -> WebDriver:
        """Creates and returns a local chrome selenium driver."""
        return webdriver.Chrome(options=options)

    @staticmethod
    def get_remote_driver(options: Options, remote_url: str) -> WebDriver:
        """Creates and returns a remote selenium driver to the specified url."""
        return webdriver.Remote(
            command_executor=remote_url,
            options=options
        )
