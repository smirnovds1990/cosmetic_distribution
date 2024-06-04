from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.exceptions import InternalServerError

from . import create_app, login_manager
from .forms import CustomerForm, OrderForm, ProductForm
from .models import Customer, Order, OrderProduct, Product, User
from .services import (
    create_customer, create_order, create_product, delete_one_order,
    get_paginated_orders, set_product_amount_to_zero
)


main_bp = Blueprint('main', __name__)


@login_manager.user_loader
def loader_user(user_id):
    """Загружает текущего пользователя из сессии. (Из док-ции Flask-Login)."""
    return User.query.get(user_id)


@main_bp.context_processor
def inject_datetime_to_templates():
    """Добавление текущего времени для доступа в шаблонах."""
    return {'now': datetime.now()}


@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form.get('username')).first()
        if not user:
            flash('Такого пользователя нет', 'error')
            return render_template('login.html')
        hashed_password = user.password
        form_password = request.form.get('password')
        if check_password_hash(hashed_password, form_password):
            login_user(user)
            return redirect(url_for('main.get_available_products'))
        else:
            flash('Неправильный пароль', 'error')
    return render_template('login.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        create_product(form=form)
        flash('Товар успешно создан.', 'success')
        return redirect(url_for('main.add_product'))
    if request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    return render_template('add_product.html', form=form)


@main_bp.route('/products')
@login_required
def get_available_products():
    products = Product.query.order_by(Product.title).filter(
        Product.amount > 0
    )
    return render_template('products.html', products=products)


@main_bp.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    method = request.form.get('_method', default='POST')
    product = Product.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        set_product_amount_to_zero(product=product)
        return redirect(url_for('main.get_available_products'))
    return redirect(url_for('main.get_available_products'))


@main_bp.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        create_customer(form=form)
        flash('Клиент успешно создан.', 'success')
        return redirect(url_for('main.add_customer'))
    return render_template('add_customer.html', form=form)


@main_bp.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    all_customers = [
        (customer.id, customer.name) for customer in
        Customer.query.order_by(Customer.name).all()
    ]
    all_products = [
        (product.id, product.title) for product in
        Product.query.order_by(Product.title).all()
    ]
    product_prices = {
        product.id: product.retail_price for product in Product.query.all()
    }
    form = OrderForm()
    form.customer.choices = [('', '---')] + all_customers
    for order_form in form.products:
        order_form.products.choices = all_products
    if form.validate_on_submit():
        create_order(form=form)
        return redirect(url_for('main.get_all_orders'))
    return render_template(
        'add_order.html', form=form, product_prices=product_prices
    )


@main_bp.route('/orders')
@login_required
def get_all_orders():
    orders = Order.query.order_by(Order.date.desc())
    page = get_paginated_orders(orders=orders)
    return render_template('orders.html', page=page)


@main_bp.route('/orders/<int:id>')
@login_required
def get_order(id):
    order = Order.query.filter_by(id=id).first_or_404()
    order_products = OrderProduct.query.filter_by(order_id=id).all()
    products = [
        Product.query.filter_by(id=op.product_id).first_or_404()
        for op in order_products
    ]
    total_sum = 0
    for order_product in order_products:
        total_sum += (order_product.quantity * order_product.price)
    context = {
        'order': order,
        'order_products': zip(order_products, products),
        'total_sum': total_sum
    }
    return render_template('order.html', context=context)


@main_bp.route('/delete_order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    method = request.form.get('_method', default='POST')
    order = Order.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        delete_one_order(order=order)
        return redirect(url_for('main.get_all_orders'))
    return redirect(url_for('main.get_all_orders'))
