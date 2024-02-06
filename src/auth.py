"""Module to manage and verify user credentials"""

import re
from flask import Blueprint, redirect, url_for, render_template, request, flash
from sqlalchemy import select
import pyscrypt
from pyisemail import is_email
from .auth_classes import SignUpForm, LoginForm
from .models import User
from . import db


auth = Blueprint("auth", __name__)

regex_email = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")  # pylint: disable=line-too-long
regex_password = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


def email_registered(email):
    """Returns True if user with given email exist"""
    return True if User.query.filter_by(email=email).first() else False


def name_registered(name):
    """Returns True if user with given email exist"""
    return True if User.query.filter_by(name=name).first() else False


def valid_email_format(string):
    """Returns True if string has email format"""

    if re.fullmatch(regex_email, string) and is_email(string):
        return True
    return False


def valid_email_dns(string):
    """Returns True if string has email format and direction is valid"""

    if re.fullmatch(regex_email, string) and is_email(string, check_dns=True):
        return True
    return False


def valid_password_format(string):
    """Returns True if string has password required requisites"""

    if re.fullmatch(regex_password, string):
        return True
    return False


def verify_signup_credentials(name, email, password):
    """Verifies validity of user given credentials"""

    if name_registered(name):
        flash("Nombre de usuario ocupado")
        return redirect(url_for("auth.signup"))

    if valid_email_dns(name):
        flash("Por favor, no use un correo electrónico como nombre de usuario")
        return redirect(url_for("auth.signup"))

    if email_registered(email):
        flash("Correo electrónico ya registrado")
        return redirect(url_for("auth.signup"))

    if not valid_email_format(email):
        flash("Correo electrónico inválido")
        return redirect(url_for("auth.signup"))

    if not valid_password_format(password):
        flash("Contraseña inválida")
        return redirect(url_for("auth.signup"))


def insert_user_db(name, email, password, avatar_id, about):
    """Inserts user in users table"""

    new_user = User(name=name,
                    email=email,
                    password=password,
                    avatar_id=avatar_id,
                    about=about)

    db.session.add(new_user)
    db.session.commit()


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

        invalid_credentials_response = verify_signup_credentials(
            name, email, password)
        if invalid_credentials_response:
            return invalid_credentials_response

        insert_user_db(name, email, password, avatar_id, about)

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


def get_user_with_name(name):
    """Get user data with name inserted"""

    return select(User).where(User.c.name == name)


def get_user_with_email(email):
    """Get user data with email inserted"""

    return select(User).where(User.c.email == email)


def password_equal_to_hashed(password, salt, hashed_password):
    """
    Verifies if password is equal to hashed_password.
    Returns boolean
    """

    password = pyscrypt.hash(password=password.encode(),
                             salt=salt.encode(),
                             N=2048,
                             r=1,
                             p=1,
                             dkLen=256)

    if password == hashed_password:
        return True

    return False


def verify_password(password, salt, hashed_password):
    """
    Verifies if password inserted is equal to hashed stored password and
    redirects to corresponding page
    """

    if not password_equal_to_hashed(password, salt, hashed_password):
        flash("Contraseña incorrecta")
        return redirect(url_for("auth.signup"))


def verify_credentials_with_email(email, password):
    """Verifies credentials using email"""

    if not email_registered(email):
        flash("El correo electrónico no se encuentra registrado")
        return redirect(url_for("auth.signup"))

    user = get_user_with_email(email)
    return verify_password(password, user.salt, user.password)


def verify_credentials_with_name(name, password):
    """Verifies credentials using name"""

    if not name_registered(name):
        flash("El nombre de usuario no se encuentra registrado")
        return redirect(url_for("auth.signup"))

    user = get_user_with_name(name)
    return verify_password(password, user.salt, user.password)


def verify_credentials(name_or_email, password):
    """Verify user credentials with database"""

    if valid_email_format(name_or_email):
        return verify_credentials_with_email(name_or_email, password)

    return verify_credentials_with_name(name_or_email, password)


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

        invalid_credentials_response = verify_credentials(
            name_or_email, password)
        if invalid_credentials_response:
            return invalid_credentials_response

        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    """
    Returns a page to confirm user logout
    Returns a response
    """

    return "Logout"
