from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
# from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from . import app, db, login_manager
from .forms import CustomerForm, OrderForm, ProductForm
from .models import Customer, Order, OrderProduct, Product, User


@login_manager.user_loader
def loader_user(user_id):
    """Загружает текущего пользователя из сессии. (Из док-ции flask-login)."""
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
        product = Product(
            title=form.title.data,
            amount=form.amount.data,
            brand=form.brand.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар успешно создан.', 'success')
        return redirect(url_for('add_product'))
    if request.method == 'POST':
        flash('Форма заполнена неврено.', 'error')
    return render_template('add_product.html', form=form)


@app.route('/products')
@login_required
def get_available_products():
    products = Product.query.order_by(Product.title).all()
    return render_template('products.html', products=products)


@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    method = request.form.get('_method', default='POST')
    product = Product.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('get_available_products'))
    return redirect(url_for('get_available_products'))


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data)
        db.session.add(customer)
        db.session.commit()
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
        return redirect(url_for('get_all_orders'))
    return render_template('add_order.html', form=form)


@app.route('/orders')
@login_required
def get_all_orders():
    orders = Order.query.order_by(Order.date.desc())
    page = db.paginate(orders, per_page=5)
    return render_template('orders.html', page=page)


@app.route('/delete_order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    method = request.form.get('_method', default='POST')
    order = Order.query.filter_by(id=id).first_or_404()
    if method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for('get_all_orders'))
    return redirect(url_for('get_all_orders'))


# Only for administration! To create a new user. Don't delete!
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         password = request.form.get('password')
#         if not password or len(password) < 8:
#             flash('Введите пароль не менее 8 символов.')
#         else:
#             hashed_password = generate_password_hash(password)
#             try:
#                 user = User(
#                     username=request.form.get('username'),
#                     password=hashed_password
#                 )
#                 db.session.add(user)
#                 db.session.commit()
#                 return redirect(url_for('login'))
#             except IntegrityError:
#                 db.session.rollback()
#                 flash('Пользователь с таким именем уже существует.')
#     return render_template('sign_up.html')
