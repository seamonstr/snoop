from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange


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
