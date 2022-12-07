from flask import Flask
from flask_migrate import Migrate
from backend.ext import db

migrate = Migrate()


def configure(app: Flask):
    migrate.init_app(app, db)
