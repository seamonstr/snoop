import logging
import pytest
import flask


logger = logging.getLogger(__name__)


def test_login_get_returns_form(app_with_temp_db: flask.Flask):
    """
    GIVEN a configured application
    WHEN a GET is made to the login URL
    THEN the login form is served with all expected fields present
    """
    expected = [b"username", b"password", b"remember_me", b"csrf_token"]
    found = set()
    with app_with_temp_db.test_client() as c:
        response = c.get("/login/")
        assert response.status_code == 200
        for respo in response.response:
            for exp in expected:
                if respo.find(exp):
                    found.add(exp)
        assert len(found) == len(expected), f"Fewer than expected fields found: {found}"


@pytest.mark.parametrize(
    "uname,password,next,exp_status,exp_redirect,exp_flash",
    [
        ("bob@bob.com", "password", None, 302, "/", False),
        ("bob@bob.com", "password", "/hello", 302, "/hello", False),
        ("baduname@bob.com", "password", None, 401, None, True),
        ("bob@bob.com", "bad_password", None, 401, None, True),
        ("baduname@bob.com", "password", "/hello", 401, None, True),
        ("bob@bob.com", "bad_password", "/hello", 401, None, True),
    ],
)
def test_login_happy_path(
    app_with_users: flask.Flask,
    uname: str,
    password: str,
    next: str,
    exp_status: int,
    exp_redirect: str,
    exp_flash: bool,
):
    """
    GIVEN a datatabase with some valid users and passwords
    WHEN a login form is submitted with a valid username and password
    THEN the user is redirected to the correct location

    GIVEN a database with some valid users and passwords
    WHEN a login form is submitted with invalid username or password
    THEN the user is redirected back to the login form with the "next" link intact
    """
    with app_with_users.test_client() as c:
        # Get the form to set the "next" in the session
        login_url = "/login/" + (f"?next={next}" if next else "")
        logger.info("Url: " + login_url)
        c.get(login_url)
        response = c.post(
            login_url,
            data={"username": uname, "pwd": password, "csrf_token": c.csrf_token},
        )
        redir = response.headers.get("Location", None)
        logger.info(redir)
        logger.info(response.status_code)
        assert (
            redir == exp_redirect
        ), "Post-login redirect not correctly set to supplied 'next'"
        assert response.status_code == exp_status
        # This next line means not xor...
        assert (exp_flash and flask.get_flashed_messages()) or not (
            exp_flash or flask.get_flashed_messages()
        )

        c.get("/logout/")
