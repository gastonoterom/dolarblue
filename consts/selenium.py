"""Constants related to selenium functionality."""

from os import environ

REMOTE_SELENIUM_URL = environ.get("REMOTE_SELENIUM_URL")

HEADLESS_SELENIUM: bool
if environ.get("HEADLESS_SELENIUM") == "false":
    HEADLESS_SELENIUM = False
else:
    HEADLESS_SELENIUM = True
