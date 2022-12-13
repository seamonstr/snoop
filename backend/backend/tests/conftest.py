# Taken from https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72

import logging
import os
import tempfile
import flask
from flask.testing import FlaskClient as BaseFlaskClient
import flask_migrate
from flask_wtf.csrf import generate_csrf
import pytest

from backend.app import create_app
from backend.blueprints.login.models import User

logger = logging.getLogger(__name__)


# A fake response class that we can use to hook the saving of the session
# to the response; enables us to grab the session cookie (which includes the
# freshly set CSRF token) and push it into our test client.
# Implements just enough interface to satisfy the call to save_session().
class ResponseShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """

    def __init__(self, client):
        self.client = client
        self.vary = set()

    def set_cookie(self, key, value="", *args, **kwargs):
        "Set the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs
        )

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(server_name, key=key, *args, **kwargs)


# We're going to extend Flask's built-in test client class, so that it knows
# how to look up CSRF tokens for you!
class FlaskClient(BaseFlaskClient):
    @property
    def csrf_token(self):
        # First, we'll wrap our request shim around the test client, so that
        # it will work correctly when Flask asks it to set a cookie.
        response = ResponseShim(self)

        # Next, we need to look up any cookies that might already exist on
        # this test client, such as the secure cookie that powers `flask.session`,
        # and make a test request context that has those cookies in it.
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)
        with flask.current_app.test_request_context(
            "/login",
            environ_overrides=environ_overrides,
        ):
            # Now, we call Flask-WTF's method of generating a CSRF token...
            csrf_token = generate_csrf()
            # ...which also sets a value in `flask.session`, so we need to
            # ask Flask to save that value to the cookie jar in the test
            # client. This is where we actually use that request shim we made!
            flask.current_app.session_interface.save_session(
                flask.current_app, flask.session, response
            )
            # And finally, return that CSRF token we got from Flask-WTF.
            return csrf_token

    # Feel free to define other methods on this test client. You can even
    # use the `csrf_token` property we just defined, like we're doing here!
    def login(self, email, password):
        return self.post(
            "/login",
            data={
                "email": email,
                "password": password,
                "csrf_token": self.csrf_token,
            },
            follow_redirects=True,
        )

    def logout(self):
        return self.get("/logout", follow_redirects=True)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def app_with_temp_db(db_config: dict) -> flask.Flask:
    """
    Application object with a usable but empty DB, CSRF-enabled.
    """
    app = create_app(**db_config, env="default")
    app.test_client_class = FlaskClient

    # Apply migrations to create the database
    with app.app_context():
        flask_migrate.upgrade()

    return app


@pytest.fixture(scope="module")
def app_with_users(app_with_temp_db: flask.Flask) -> flask.Flask:
    """
    Provides an app object with a configured set of users that can
    actually be logged-in to
    """

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


def delete_me():
    """
    Ignorable - will be deleted
    """

    # To hook up this extended test client class to your Flask application,
    # assign it to the `test_client_class` property, like this:
    app = flask.Flask(__name__)
    app.test_client_class = FlaskClient

    # Now in your tests, you can request a test client the same way
    # that you normally do:
    client = app.test_client()
    # But now, `client` is an instance of the class we defined!

    # In your tests, you can call the methods you defined, like this:
    client.login("user@example.com", "passw0rd")

    # And any time you need to pass a CSRF token, just use the `csrf_token`
    # property, like this:
    client.post(
        "/user/1",
        data={
            "favorite_color": "blue",
            "csrf_token": client.csrf_token,
        },
    )
