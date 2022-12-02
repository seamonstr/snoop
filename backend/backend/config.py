import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEFAULT_BCRYPT_HASH = "959561b0-6cc6-11ed-bd7b-93a916ce9dac"
DEV = "development"


class Config:
    SECRET_KEY = os.environ.get("BCRYPT_HASH", DEFAULT_BCRYPT_HASH)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENVIRONMENT = os.environ.get("ENVIRONMENT", DEV)
