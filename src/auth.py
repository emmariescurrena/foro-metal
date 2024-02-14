"""Module to manage and verify user credentials"""

from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, login_required, logout_user
from .auth_classes import SignUpForm, LoginForm
from .auth_queries import insert_user_db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Renders and returns template for sign up
    Returns a string
    """

    form = SignUpForm(request.form)
    if form.validate_on_submit():

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        avatar_id = request.form.get("avatar_id")
        about = request.form.get("about")

        user = User(name=name,
                    email=email,
                    password=password,
                    avatar_id=avatar_id,
                    about=about)

        insert_user_db(user)

        return redirect(url_for("main.index"))

    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders a template for login
    Returns a string
    """

    form = LoginForm(request.form)
    if form.validate_on_submit():

        remember = True if request.form.get("remember") else False
        login_user(form.user, remember=remember)
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """
    Returns a page to confirm user logout
    Returns a response
    """

    logout_user()
    return redirect(url_for("main.index"))
