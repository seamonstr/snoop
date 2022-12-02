import structlog
import flask
from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from .app import app

logger = structlog.get_logger(__name__)


class Bloke:
    def __init__(self, name="", age="") -> None:
        self.name = name
        self.age = age


the_bloke = Bloke("Boris", "47")


class BlokeForm(Form):
    name = StringField(
        validators=[
            DataRequired("Name is required"),
            Length(10, 20, "Name is between 10 and 20 chars"),
        ]
    )
    age = IntegerField(
        validators=[NumberRange(10, 110, "That person is either a child or dead")]
    )

    def validate_age(form, field):
        if form.data == 42:
            raise ValidationError("Age is not the answer")


@app.route("/")
def root():
    return flask.render_template("index.html")


@app.route("/bloke/", defaults={"bloke_id": None}, methods=["GET", "POST"])
@app.route("/bloke/<int:bloke_id>", methods=["GET", "POST"])
def edit_bloke(bloke_id: int):
    if flask.request.method == "GET":
        if bloke_id is None:
            form = BlokeForm()
        else:
            form = BlokeForm(obj=the_bloke)
    else:
        # POST: Validate the data
        logger.info(f"Args are {flask.request.form}")
        form = BlokeForm(flask.request.form)
        if form.validate():
            logger.info(f"Wrote a {'new ' if bloke_id is None else '' }bloke")
            return flask.redirect(app.url_for("edit_bloke", bloke_id=bloke_id))

    assert form, "Should have a form object here!"
    return flask.render_template("bloke.html", form=form, bloke_id=bloke_id)
