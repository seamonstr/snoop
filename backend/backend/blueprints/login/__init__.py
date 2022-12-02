from flask import Blueprint
from importlib import import_module

login_blueprint = Blueprint(
    "login", __name__, template_folder="templates", static_folder="static"
)

import_module(".routes", __package__)
