from flask import redirect, render_template, request, url_for
from flask_login import login_user

from . import app, db, login_manager
from .models import User


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = User(
            username=request.form.get("username"),
            password=request.form.get("password")
        )
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("home"))
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")


@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")
