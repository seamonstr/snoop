from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def configure(app: Flask):
    bcrypt.init_app(app)
