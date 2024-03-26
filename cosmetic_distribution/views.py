from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
# from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from . import app, db, login_manager
from .forms import CustomerForm, ProductForm
from .models import Customer, Product, User


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
            volume=form.volume.data,
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


@app.route('/<int:id>', methods=['POST'])
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
