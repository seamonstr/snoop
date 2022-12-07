from flask_login import UserMixin
import flask
from backend.ext import db


class User(db.Model, UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, pwd: str) -> bool:
        return flask.current_app.bcrypt.check_password_hash(self.pwd, pwd)
