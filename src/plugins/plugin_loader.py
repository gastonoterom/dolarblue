import os
import importlib
import logging
from typing import Callable,  Set, Tuple

plugins: Set[Tuple[str, Callable[[], Tuple[float, float]]]] = set()


def load_plugins() -> None:
    """Loads all the dolarblue plugins in this modules folder"""

    base_path = "./src/plugins/dolarblue_sources"

    module_names: Set[str] = {
        f.name.replace(".py", "")
        for f in os.scandir(base_path)
        if f.is_file() and f.name != "__init__.py"
    }

    modules = map(
        lambda module: importlib.import_module(
            "src.plugins.dolarblue_sources."+module),
        module_names
    )

    for module in modules:
        try:
            # Check that the module has a get_plugin function

            # Ignore the typing in this lines until a better way to predict runtime loaded modules
            # type is found

            assert module.get_plugin is not None  # type: ignore
            plugins.add(module.get_plugin())  # type: ignore

            logging.info("Success loading plugin %s", module.__name__)
        except AttributeError:
            logging.error(
                "Error loading plugin %s, plugin has no get_plugin function", module.__name__)
        except AssertionError:
            logging.error(
                "Error loading plugin %s, invalid plugin 'get_plugin' function", module.__name__)


def get_plugins() -> Set[Tuple[str, Callable[[], Tuple[float, float]]]]:
    """Gets all the LOADED plugins from the plugins module"""
    return plugins
