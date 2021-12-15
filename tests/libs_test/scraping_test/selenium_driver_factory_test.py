# pylint: disable=missing-docstring

import subprocess
import unittest
from time import sleep

from selenium.webdriver.chrome.options import Options
from libs.scraping.selenium_driver_factory import SeleniumDriverFactory
from tests.testing_consts import TESTING_SELENIUM_URL

class TestSeleniumDriverFactory(unittest.TestCase):

    def start_docker_selenium(self) -> None:
        """Start selenium docker containers"""

        subprocess.run(
            [
                "docker", "run",
                "-d",
                "--name", "selenium-testing",
                "-p", "4445:4444",
                "selenium/standalone-chrome"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
        sleep(5)

    def stop_docker_selenium(self) -> None:
        """Finish and remove docker containers"""
        subprocess.run(
            [
                "docker", "stop",
                "selenium-testing"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            [
                "docker", "rm",
                "selenium-testing"
            ],
            check=True,
            stdout=subprocess.DEVNULL
        )

    def test_selenium_local_driver(self) -> None:

        driver = SeleniumDriverFactory.get_driver()

        driver.close()
        driver.quit()

    def test_selenium_remote_driver(self) -> None:
        try:
            self.start_docker_selenium()
            driver = SeleniumDriverFactory.get_driver(TESTING_SELENIUM_URL)

        finally:
            if driver:
                driver.close()
                driver.quit()

            self.stop_docker_selenium()

    def test_selenium_driver_with_options(self) -> None:

        options = Options()
        options.headless = True
        options.add_argument("--silent")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = SeleniumDriverFactory.get_driver(options=options)

        driver.close()
        driver.quit()
