import structlog
import flask
from flask import url_for

from . import login_blueprint
from .models import Bloke
from .forms import BlokeForm

logger = structlog.get_logger(__name__)

the_bloke = Bloke("Boris", "47")


@login_blueprint.route("/bloke/", defaults={"bloke_id": None}, methods=["GET", "POST"])
@login_blueprint.route("/bloke/<int:bloke_id>", methods=["GET", "POST"])
def edit_bloke(bloke_id: int):
    if flask.request.method == "GET":
        if bloke_id is None:
            form = BlokeForm()
        else:
            form = BlokeForm(obj=the_bloke)
    else:
        # POST: Validate the data
        form = BlokeForm(flask.request.form)
        if form.validate():
            logger.info(f"Wrote a {'new ' if bloke_id is None else '' }bloke")
            bloke_id = 42  # would write a new one
            return flask.redirect(url_for(".edit_bloke", bloke_id=bloke_id))

    assert form, "Should have a form object here!"
    return flask.render_template("bloke.html", form=form, bloke_id=bloke_id)
