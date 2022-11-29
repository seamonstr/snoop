from flask_login import UserMixin
from backend.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'