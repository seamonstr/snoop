import os

from logging.config import fileConfig

from sys import modules


def backend_modules_present(ignore: list[str]) -> bool:
    """
    Return the first loaded module found that is a child of the "backend"
    project.

    Parameters:
    ignore (list[str]): List of packages to ignore.
    """
    for i in modules:
        if i.startswith("backend.") and i not in ignore:
            return i
    return None


def configure_logging(logging_cfg: str):
    """
    Expects a logging config filename, either absolute or relative to CWD
    """

    # Check that no other modules from our app code are loaded before we've
    # configured logging.
    if backend_modules_present(ignore=["backend", "backend.logging"]):
        raise RuntimeError("Application code loaded before logging was configured")

    fileConfig(logging_cfg)


# configure the logging. Logging's config file is configured with
# an envar, uniquely, because settings.toml is only loaded much later when we
# create a Flask object.
configure_logging(os.environ.get("LOGGING_CONFIG", "logging-dev.cfg"))
