import logging
import uuid
import structlog
import sys
from datetime import datetime

import flask


def setup_logging_context():
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        view=flask.request.path,
        request_id=str(uuid.uuid4()),
        peer=flask.request.access_route[0],
        timestamp=datetime.now(),
    )


def init_app_logging(app: flask.Flask):
    """
    Insert a function to correctly set up each request's context before processing
    """
    app.before_request(setup_logging_context)


def init_logging(debug):
    """
    Initialise structlog
    """

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    if debug:
        renderer = structlog.dev.ConsoleRenderer(pad_event=30, sort_keys=True)
    else:
        renderer = structlog.processors.LogfmtRenderer(
            key_order=["event", "view", "peer"]
        )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.ExceptionPrettyPrinter(),
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
