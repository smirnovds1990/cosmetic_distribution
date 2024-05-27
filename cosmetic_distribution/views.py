from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from . import app, login_manager
from .forms import CustomerForm, OrderForm, ProductForm
from .models import Customer, Order, OrderProduct, Product, User
from .services import (
    create_customer, create_order, create_product, delete_obj,
    get_paginated_orders
)


@login_manager.user_loader
def loader_user(user_id):
    """Загружает текущего пользователя из сессии. (Из док-ции Flask-Login)."""
    return User.query.get(user_id)


@app.context_processor
def inject_datetime_to_templates():
    """Добавление текущего времени для доступа в шаблонах."""
    return {'now': datetime.now()}


@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('get_available_products'))
        else:
            flash('Неправильный пароль', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        create_product(form=form)
        flash('Товар успешно создан.', 'success')
        return redirect(url_for('add_product'))
    if request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    return render_template('add_product.html', form=form)


@app.route('/products')
@login_required
def get_available_products():
    products = Product.query.order_by(Product.title).filter(
        Product.amount > 0
    )
    return render_template('products.html', products=products)


@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    method = request.form.get('_method', default='POST')
    product = Product.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        delete_obj(obj=product)
        return redirect(url_for('get_available_products'))
    return redirect(url_for('get_available_products'))


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        create_customer(form=form)
        flash('Клиент успешно создан.', 'success')
        return redirect(url_for('add_customer'))
    return render_template('add_customer.html', form=form)


@app.route('/add_order', methods=['GET', 'POST'])
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
    form = OrderForm()
    form.customer.choices = [('', '---')] + all_customers
    for order_form in form.products:
        order_form.products.choices = all_products
    if form.validate_on_submit():
        create_order(form=form)
        return redirect(url_for('get_all_orders'))
    return render_template('add_order.html', form=form)


@app.route('/orders')
@login_required
def get_all_orders():
    orders = Order.query.order_by(Order.date.desc())
    page = get_paginated_orders(orders=orders)
    return render_template('orders.html', page=page)


@app.route('/orders/<int:id>')
@login_required
def get_order(id):
    order = Order.query.filter_by(id=id).first_or_404()
    order_products = OrderProduct.query.filter_by(order_id=id).all()
    products = [
        Product.query.filter_by(id=op.product_id).first_or_404()
        for op in order_products
    ]
    context = {
        'order': order,
        'order_products': zip(order_products, products)
    }
    return render_template('order.html', context=context)


@app.route('/delete_order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    method = request.form.get('_method', default='POST')
    order = Order.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        delete_obj(obj=order)
        return redirect(url_for('get_all_orders'))
    return redirect(url_for('get_all_orders'))
