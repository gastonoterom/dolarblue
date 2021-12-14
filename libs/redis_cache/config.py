"""Constants for redis usage."""
from os import environ
from typing import cast

REDIS_HOST = cast(str, environ.get("REDIS_HOST"))
REDIS_PORT = cast(int, environ.get("REDIS_PORT"))
REDIS_DB   = cast(int, environ.get("REDIS_DB"))
