from flask import Blueprint, Flask
from importlib import import_module

login_blueprint = Blueprint(
    "login", __name__, template_folder="templates", static_folder="static"
)


def configure(app: Flask):
    app.register_blueprint(login_blueprint)


import_module(".routes", __package__)
