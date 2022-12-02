import structlog

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
)

from . import config, models
from .db import db
from .logging import init_logging, init_app_logging
from .blueprints.login import login_blueprint

init_logging(config.Config.ENVIRONMENT == config.DEV)
log = structlog.get_logger(source_module=__name__)


# Singleton factory doodads
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)


def create_app():
    app = Flask(__name__, static_url_path="")
    init_app_logging(app)

    app.config.from_object(config.Config)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(login_blueprint)
    app.add_url_rule("/", view_func=lambda: render_template("index.html"))

    return app


app = create_app()
