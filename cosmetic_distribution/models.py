from flask_login import UserMixin

from .constants import MAX_STRING_FIELD_LENGTH
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(MAX_STRING_FIELD_LENGTH), unique=True, nullable=False
    )
    password = db.Column(
        db.String(MAX_STRING_FIELD_LENGTH), nullable=False
    )
