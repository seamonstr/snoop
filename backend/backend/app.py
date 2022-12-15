from dynaconf import FlaskDynaconf

from flask import Flask, render_template

from . import blueprints, ext, logging


# Logging, as ever, is a pain.
# You should only ever configure logging once in Python, because
# reconfiguring it disables all existing loggers.

# However, dynaconf will only load the config once it has an app
# object to configure, so we can only configure the logging on the
# creation of the first app.
logging_configured = False


def create_app(**kwargs) -> Flask:
    """
    Create a new Flask app.

    kwargs are passed through to the configuration Dynaconf.
    Useful values are:
    * env: set to a section name in 'settings.toml'
    * SQLALCHEMY_DATABASE_URI: set to a filename for a temp db
    """
    app = Flask(__name__, static_url_path="")

    # Settings managed by dynaconf, taken from settings.toml
    # Set FLASK_ENV to choose the environment: development or production
    FlaskDynaconf(app, **kwargs)

    global logging_configured
    if not logging_configured:
        log_config = app.config.get("LOGGING_CFG", None)
        if log_config is None:
            raise RuntimeError("LOGGING_CFG isn't set in settings.toml")
        logging.configure_logging(log_config)
        logging_configured = True

    app.add_url_rule(
        "/", endpoint="index", view_func=lambda: render_template("index.html")
    )

    blueprints.register_blueprints(app)
    ext.register_extensions(app)

    return app


# TODO: this should be factored away
app = create_app()
