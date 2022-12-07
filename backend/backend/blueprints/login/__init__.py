from importlib import import_module

from flask import Blueprint, Flask
from flask_login import LoginManager

from .models import User

# Login manager initialisation
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Blueprint initialisation
login_blueprint = Blueprint(
    name="login",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)


def configure(app: Flask):
    app.register_blueprint(login_blueprint)
    login_manager.init_app(app)


import_module(".routes", __package__)
