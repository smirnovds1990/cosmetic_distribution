from . import db
from .models import Customer, Order, OrderProduct, Product


def create_product(form):
    product = Product.query.filter_by(title=form.title.data).first()
    if not product:
        product = Product(
            title=form.title.data,
            amount=form.amount.data,
            brand=form.brand.data,
            wholesale_price=form.wholesale_price.data,
            retail_price=form.retail_price.data
        )
    else:
        product.amount += form.amount.data
        product.brand = form.brand.data
        product.wholesale_price = form.wholesale_price.data
        product.retail_price = form.retail_price.data
    db.session.add(product)
    db.session.commit()


def create_customer(form):
    customer = Customer(name=form.name.data)
    db.session.add(customer)
    db.session.commit()


def create_order(form):
    new_order = Order(customer_id=form.customer.data)
    db.session.add(new_order)
    db.session.commit()
    for product_data in form.products.data:
        product_id = (
            Product.query.filter_by(
                id=product_data['products']
                ).first_or_404()
        )
        storage_quantity = product_id.amount
        order_quantity = product_data['quantity']
        new_quantity = storage_quantity - order_quantity
        product_id.amount = new_quantity
        new_order_product = OrderProduct(
            order_id=new_order.id,
            product_id=product_data['products'],
            quantity=product_data['quantity'],
            price=product_data['price']
        )
        db.session.add(new_order_product)
    db.session.commit()


def delete_obj(obj):
    db.session.delete(obj)
    db.session.commit()


def get_paginated_orders(orders):
    return db.paginate(orders, per_page=5)
