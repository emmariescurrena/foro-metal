"""Module to manage and verify user credentials"""

from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, login_required, logout_user
from bcrypt import checkpw
from .auth_classes import SignUpForm, LoginForm
from .models import User
from . import db

auth = Blueprint("auth", __name__)


def insert_user_db(name, email, password, avatar_id, about):
    """Inserts new user in users table"""

    new_user = User(name=name,
                    email=email,
                    password=password,
                    avatar_id=avatar_id,
                    about=about)

    db.session.add(new_user)
    db.session.commit()


def get_user_with_email(email):
    """Get user data with email given"""

    return User.query.filter_by(email=email).first()


def get_user_with_name(name):
    """Get user data with name given"""

    return User.query.filter_by(name=name).first()


def verify_user_exists_with_email(email):
    """Verifies login credentials with given email"""

    if not email_registered(email):
        flash("El correo electrónico no se encuentra registrado")
        return redirect(url_for("auth.login"))


def verify_user_exists_with_name(name):
    """Verifies login credentials with given name"""

    if not name_registered(name):
        flash("El nombre de usuario no se encuentra registrado")
        return redirect(url_for("auth.login"))


def validate_signup(form):
    """Validates aspects that wtforms can't"""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    avatar_id = request.form.get("avatar_id")
    about = request.form.get("about")

    return verify_signup_credentials(name, email, password)


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

        error_response = verify_signup_credentials(name, email, password)
        if error_response:
            return error_response

        insert_user_db(name, email, password, avatar_id, about)

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders a template for login
    Returns a string
    """

    form = LoginForm(request.form)
    if form.validate_on_submit():

        name_or_email = request.form.get("name_or_email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if valid_email_format(name_or_email):
            email = name_or_email
            user_not_found_response = verify_user_exists_with_email(email)
            user = get_user_with_email(email)
        else:
            name = name_or_email
            user_not_found_response = verify_user_exists_with_name(name)
            user = get_user_with_name(name)

        if user_not_found_response:
            return user_not_found_response

        hashed_password = user.password
        if not checkpw(password.encode("utf8"), hashed_password):
            flash("Contraseña incorrecta")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
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
