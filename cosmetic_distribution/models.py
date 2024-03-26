from datetime import datetime

from flask_login import UserMixin

from .constants import (
    DEFAULT_AMOUNT, MAX_PRODUCT_VOLUME_LENGTH, MAX_STRING_FIELD_LENGTH
)
from . import db


order_products = db.Table(
    'order_products',
    db.Column(
        'order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True
    ),
    db.Column(
        'product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True
    ),
    db.Column('quantity', db.Integer, nullable=False),
    db.Column('price', db.Integer, nullable=False)
)


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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=True
    )
    products = db.relationship(
        'Product', secondary=order_products, backref='order'
    )


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STRING_FIELD_LENGTH), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)
