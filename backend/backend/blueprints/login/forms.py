from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import (
    Email,
    Length,
    DataRequired,
    EqualTo,
    ValidationError,
)

from .models import User


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
    remember_me = BooleanField()
    pwd = PasswordField(validators=[DataRequired(), Length(8, 72)])
