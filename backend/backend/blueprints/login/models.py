from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from backend.ext import db


class User(db.Model, UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    pwd_hash = db.Column(db.String(300), nullable=False, unique=True)

    def __init__(self, **kwargs):
        password = kwargs.get("password")
        if password:
            if "pwd_hash" in kwargs:
                raise ValueError("Specify only one of password or pwd_hash")
            kwargs.pop("password")

        db.Model.__init__(self, **kwargs)
        if password:
            self.set_hash_from_password(password)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_hash_from_password(self, password: str):
        self.pwd_hash = generate_password_hash(password)

    def check_password_hash(self, candidate: str) -> bool:
        """
        If the password is None or empty, return false.
        Otherwise, return the result of checking the candidate
        password against the stored hash.
        """
        return candidate and check_password_hash(self.pwd_hash, candidate)
