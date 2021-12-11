"""Selenium driver factory for a local or remote driver."""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from consts.selenium_values import HEADLESS_SELENIUM


class SeleniumDriverFactory():
    """This class has static methods for constructing selenium driver objects."""

    @staticmethod
    def get_driver(remote_url:Optional[str] = None, options: Optional[Options] = None) -> WebDriver:
        """Creates and returns a local or remote selenium driver,
        depending if the remote url was given or not,
        if options not given it just returns a headless driver"""

        if options is None:
            options = Options()
            options.headless = HEADLESS_SELENIUM
            options.add_argument("--silent")
            options.add_argument("--log-level=3")
        if remote_url:
            return SeleniumDriverFactory.get_remote_driver(options, remote_url)
        else:
            return SeleniumDriverFactory.get_local_driver(options)

    @staticmethod
    def get_local_driver(options: Options) -> WebDriver:
        """Creates and returns a local chrome selenium driver."""

        return webdriver.Chrome(options=options)

    @staticmethod
    def get_remote_driver(options: Options, remote_url: str) -> WebDriver:
        """Creates and returns a remote selenium driver to the specified url."""

        return webdriver.Remote(remote_url, options.to_capabilities())
