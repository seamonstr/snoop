from dynaconf import FlaskDynaconf

from flask import Flask, render_template

from . import blueprints, ext


def create_app():
    app = Flask(__name__, static_url_path="")

    # Settings managed by dynaconf; pulled from settings.toml
    # Set FLASK_ENV to choose the environment: development or production
    FlaskDynaconf(app)

    app.add_url_rule(
        "/", endpoint="index", view_func=lambda: render_template("index.html")
    )

    blueprints.register_blueprints(app)
    ext.register_extensions(app)

    return app


app = create_app()
