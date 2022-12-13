import os
import tempfile
import logging

import flask
import flask_migrate
import pytest

from backend.app import create_app
from backend.blueprints.login.models import User

logger = logging.getLogger(__name__)


@pytest.fixture
def db_config():
    db_fd, fn = tempfile.mkstemp()
    try:
        # Results in four slashes; this is expected, as the URl
        # format is "sqlite://<nohostname>/<path>", and <path>
        # starts with a slash.
        yield {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{fn}"}
    finally:
        os.close(db_fd)
        os.unlink(fn)


@pytest.fixture
def app_with_temp_db(db_config: dict) -> flask.Flask:
    app = create_app(**db_config, env="default")

    # Apply migrations
    with app.app_context():
        flask_migrate.upgrade()

    return app


@pytest.fixture
def app_with_users(app_with_temp_db: flask.Flask) -> flask.Flask:
    def insert_user(user_data: dict):
        u = User(**user_data)
        logger.debug(f"Adding user {u.username}")
        db.session().add(u)

    with app_with_temp_db.app_context():
        db = app_with_temp_db.extensions["sqlalchemy"]

        for u in [
            {"username": "bob@bob.com", "password": "password"},
            {"username": "two@bob.com", "password": "password2"},
        ]:
            insert_user(u)

        db.session().commit()
    return app_with_temp_db


def test_login_get_returns_form(app_with_users: flask.Flask):
    """
    GIVEN a configured application
    WHEN a GET is made to the login URL
    THEN the login form is served
    """
    expected = [b"username", b"password", b"remember_me"]
    found = set()
    with app_with_users.test_client() as c:
        response = c.get("/login/")
        assert response.status_code == 200
        for respo in response.response:
            for exp in expected:
                if respo.find(exp):
                    found.add(exp)
        assert len(found) == len(expected), f"Fewer than expected fields found: {found}"
