# It's really important that we configure logging here, and that no other
# app modules get loaded before logging is configured.

# It uses fileConfig() to configure logging for the server, and fileConfig()
# permanently disables all existing loggers for reasons best known to its
# authors.
#
# Thus, any loggers created before calling fileConfig() (eg. at
# global scope in their respective modules, so created at import time) will
# just mysteriously go silent.
#
# This is here on its own import line so that it doesn't accidentally get something
# inserted before it.
from . import logging  # noqa: F401

# Ignore flake8 complaint; this has to be after the logging configuration.
from . import app

app = app.app
