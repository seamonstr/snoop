from flask import url_for, flash, redirect, render_template, current_app, request
from flask_login import login_user, logout_user, current_user

from .forms import LoginForm
from .models import User
from backend.utils import is_safe_url

from . import login_blueprint


def _get_next_url():
    """
    Return a redirect reponse object to the URL in the current
    request's 'next' arg, if that URL is safe to redirect to.
    Otherwise, redirect to '/'.
    """
    next = request.args.get("next")
    if next and not is_safe_url(next):
        current_app.logger.info(f"Dangerous redirect attempt: {next}")
        next = None
    return redirect(next or url_for("index"))


@login_blueprint.route("/login/", methods=["POST", "GET"])
def login():
    current_app.logger.debug("In login handler...")
    if current_user.is_authenticated:
        flash("already logged in")
        return _get_next_url()

    form = LoginForm()
    if request.method == "GET":
        status = 200
    else:
        status = 401
        # the validation process sets error messages on any field in the form
        # whose validation fails; they're rendered in the call to the template below.
        if form.validate_on_submit():
            current_app.logger.debug("Form validated")
            user = User.query.filter_by(username=form.username.data).first()
            current_app.logger.debug(f"Got user {user}")

            if user and user.check_password_hash(form.pwd.data):
                current_app.logger.debug("Login success")
                login_user(user, remember=form.remember_me.data)
                return _get_next_url()
            else:
                current_app.logger.info(
                    f"Failed login for {form.username.data}: {'No such user' if not user else user.id}"
                )
                flash("Invalid username or password")

    return (
        render_template(
            "login.html",
            form=form,
        ),
        status,
    )


@login_blueprint.route("/logout/", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))
