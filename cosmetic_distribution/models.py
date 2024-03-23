from flask_login import UserMixin
from sqlalchemy import CheckConstraint

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
    title_en = db.Column(db.String(MAX_STRING_FIELD_LENGTH))
    title_rus = db.Column(db.String(MAX_STRING_FIELD_LENGTH), nullable=False)
    volume = db.Column(db.String(MAX_PRODUCT_VOLUME_LENGTH), nullable=False)
    amount = db.Column(db.Integer, default=DEFAULT_AMOUNT)
    brand = db.Column(db.String(MAX_STRING_FIELD_LENGTH))

    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_positive_amount'),
    )
