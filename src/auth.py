"""Module to manage and verify user credentials"""

import re
from flask import Blueprint, redirect, url_for, render_template, request, flash
from sqlalchemy import select
from bcrypt import checkpw
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

    return True if re.fullmatch(regex_email, string) and is_email(string) else False


def valid_email_dns(string):
    """Returns True if string has email format and direction is valid"""

    return True if re.fullmatch(regex_email, string) and is_email(string, check_dns=True) else False


def valid_password_format(string):
    """Returns True if string has password required requisites"""

    return True if re.fullmatch(regex_password, string) else False


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

        error_response = verify_signup_credentials(name, email, password)
        if error_response:
            return error_response

        insert_user_db(name, email, password, avatar_id, about)

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


def get_user_credentials(name_or_email):
    """Get user data with email inserted"""

    stmt = (
        select(User.password)
        .filter((User.name == name_or_email) | (User.email == name_or_email))
    )
    result = db.session.execute(stmt)
    hashed_password = result.one().password

    return hashed_password


def verify_password(password, hashed_password):
    """
    Verifies if password inserted is equal to hashed stored password and
    redirects to corresponding page
    """

    if not checkpw(password.encode("utf8"), hashed_password):
        flash("Contraseña incorrecta")
        return redirect(url_for("auth.login"))


def verify_login_credentials(name_or_email, password):
    """Verifies user credentials with database"""

    if valid_email_format(name_or_email):
        if not email_registered(name_or_email):
            flash("El correo electrónico no se encuentra registrado")
            return redirect(url_for("auth.login"))

    else:
        if not name_registered(name_or_email):
            flash("El nombre de usuario no se encuentra registrado")
            return redirect(url_for("auth.login"))

    hashed_password = get_user_credentials(name_or_email)

    return verify_password(password, hashed_password)


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

        error_response = verify_login_credentials(name_or_email, password)
        if error_response:
            return error_response

        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@auth.route("/perfil")
def profile():
    """
    Renders template for perfil
    Returns a string
    """

    return render_template("perfil.html")


@auth.route("/logout")
def logout():
    """
    Returns a page to confirm user logout
    Returns a response
    """

    return "Logout"
