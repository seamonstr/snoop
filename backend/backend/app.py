from dynaconf import FlaskDynaconf

from flask import Flask, render_template

from . import blueprints, ext


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

    app.add_url_rule(
        "/", endpoint="index", view_func=lambda: render_template("index.html")
    )

    blueprints.register_blueprints(app)
    ext.register_extensions(app)

    return app


# TODO: this should be factored away
app = create_app()
