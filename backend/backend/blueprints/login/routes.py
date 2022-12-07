from flask import url_for, flash, redirect, render_template, current_app
from flask_login import login_user, current_user

from .forms import LoginForm
from .models import User

from . import login_blueprint


@login_blueprint.route("/login/", methods=["POST", "GET"])
def login():
    current_app.logger.debug("In login handler...")
    if current_user.is_authenticated:
        flash("already logged in")
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.debug("Form validated")

        user = User.query.filter_by(username=form.username.data).first()
        current_app.logger.debug(f"Got user {user}")

        if user is None or not user.check_password(form.pwd.data):
            current_app.logger.info(
                f"Failed login for {user.username}: {'No user' if not user else user.id}"
            )
            flash("Invalid username or password")
            return redirect(url_for("login.login"))
        current_app.logger.debug("Login success")

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))

    return render_template("login.html", form=form)
