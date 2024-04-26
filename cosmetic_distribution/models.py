from datetime import datetime

from flask_login import UserMixin

from .constants import (
    DEFAULT_AMOUNT, MAX_STRING_FIELD_LENGTH, POSITIVE_INT_DEFAULT
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
    amount = db.Column(db.Integer, default=DEFAULT_AMOUNT)
    brand = db.Column(db.String(MAX_STRING_FIELD_LENGTH))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=True
    )
    products = db.relationship(
        'Product', secondary='order_product', backref='order'
    )


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STRING_FIELD_LENGTH), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __str__(self):
        return self.name


class OrderProduct(db.Model):
    """Вспомогательная модель для продуктов в заказе."""
    order_id = db.Column(
        db.Integer, db.ForeignKey('order.id'), primary_key=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), primary_key=True
    )
    quantity = db.Column(
        db.Integer, default=POSITIVE_INT_DEFAULT, nullable=False
    )
    price = db.Column(
        db.Integer, default=POSITIVE_INT_DEFAULT, nullable=False
    )
