from dynaconf import FlaskDynaconf

from flask import Flask, render_template
from flask_login import (
    LoginManager,
)

from . import models, blueprints, ext


def create_app():
    app = Flask(__name__, static_url_path="")

    # Settings managed by dynaconf; pulled from settings.toml
    # Set FLASK_ENV to choose the environment: development or production
    FlaskDynaconf(app)

    login_manager.init_app(app)

    app.add_url_rule("/", view_func=lambda: render_template("index.html"))

    blueprints.register_blueprints(app)
    ext.register_extensions(app)

    return app


# Singleton factory doodads
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)


app = create_app()
