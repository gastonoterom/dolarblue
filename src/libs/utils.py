
import time
import logging
from typing import Any, Callable


def log_runtime(function_to_log: Callable) -> Callable:
    """This decorator logs the runtime of the decorated function"""
    def check_time(*args, **kwargs) -> Any:
        start = time.perf_counter()
        rsp = function_to_log(*args, **kwargs)
        elapsed = time.perf_counter() - start

        logging.info("%s executed in %s seconds",
                     function_to_log.__name__, str(round(elapsed, 10)))

        return rsp

    return check_time
