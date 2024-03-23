from flask_login import UserMixin

from .constants import (
    DEFAULT_AMOUNT, MAX_PRODUCT_VOLUME_LENGTH, MAX_STRING_FIELD_LENGTH
)
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(MAX_STRING_FIELD_LENGTH), unique=True, nullable=False
    )
    password = db.Column(
        db.String(MAX_STRING_FIELD_LENGTH), nullable=False
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(MAX_STRING_FIELD_LENGTH), nullable=False)
    volume = db.Column(db.String(MAX_PRODUCT_VOLUME_LENGTH), nullable=False)
    amount = db.Column(db.Integer, default=DEFAULT_AMOUNT)
    brand = db.Column(db.String(MAX_STRING_FIELD_LENGTH))

    def __str__(self):
        return f'{self.title} {self.volume} - {self.amount}шт'
