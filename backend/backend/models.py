from flask_login import UserMixin
from backend.ext import db_engine


class User(db_engine.Model, UserMixin):  # type: ignore
    id = db_engine.Column(db_engine.Integer, primary_key=True)
    username = db_engine.Column(db_engine.String(80), unique=True, nullable=False, index=True)
    pwd = db_engine.Column(db_engine.String(300), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
