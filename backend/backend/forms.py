from wtforms import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
)
from wtforms.validators import (
    Email,
    Length,
    DataRequired,
    EqualTo,
    Optional,
    ValidationError,
)

from backend.models import User


class RegistrationForm(FlaskForm):

    username = StringField(
        validators=[
            DataRequired(),
            Email(message="Username must be a valid email address"),
        ]
    )
    pwd = PasswordField(validators=[DataRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            EqualTo("pwd", message="Passwords must match"),
        ]
    )

    def validate_username(self, field):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("That username is already in use")


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Email()])
    pwd = PasswordField(validators=[DataRequired(), Length(8, 72)])

    username = StringField(validators=[Optional()])
