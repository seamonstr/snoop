from flask import Flask
from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy()


def configure(app: Flask):
    engine.init_app(app)
