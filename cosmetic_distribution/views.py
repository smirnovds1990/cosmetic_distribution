from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
# from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

from . import app, db, login_manager
from .models import User


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


# Only for administration! To create a new user. Don't delete!
# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         password = request.form.get("password")
#         if not password or len(password) < 8:
#             flash('Введите пароль не менее 8 символов.')
#         else:
#             hashed_password = generate_password_hash(password)
#             try:
#                 user = User(
#                     username=request.form.get("username"),
#                     password=hashed_password
#                 )
#                 db.session.add(user)
#                 db.session.commit()
#                 return redirect(url_for("login"))
#             except IntegrityError:
#                 db.session.rollback()
#                 flash('Пользователь с таким именем уже существует.')
#     return render_template("sign_up.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if not user:
            flash('Такого пользователя нет', 'error')
            return render_template("login.html")
        hashed_password = user.password
        form_password = request.form.get("password")
        if check_password_hash(hashed_password, form_password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash('Неправильный пароль', 'error')
    return render_template("login.html")
