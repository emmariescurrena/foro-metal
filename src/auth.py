"""Module to manage and verify user credentials"""

from flask import Blueprint, redirect, url_for, render_template, request
from wtforms import Form, StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired
from . import db

auth = Blueprint("auth", __name__)


class SignUpForm(Form):
    """Form for sign up"""
    name = StringField(
        "Nombre de usuario*",
        validators=[
            InputRequired(),
            Length(min=4, max=30)
        ]
    )
    email = StringField(
        "Correo electrónico*",
        validators=[
            InputRequired(),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        "Contraseña*",
        validators=[
            InputRequired(),
            Length(min=8, max=72),
        ]
    )
    confirm = PasswordField(
        "Confirmar contraseña*",
        validators=[
            InputRequired(),
            EqualTo(
                'password',
                message='Las contraseñas deben ser iguales'
            )
        ]
    )
    about = StringField(
        "Frase que te describa",
        widget=TextArea(),
        validators=[Length(max=256)]
    )


@auth.route("/signup", methods=["POST"])
def signup():
    """
    Renders and returns template for sign up
    Returns a string
    """

    form = SignUpForm(request.form)
    return render_template("signup.html", form=form)


@auth.route("/signup", methods=["POST"])
def signup_post():
    """
    Renders a page to confirm user's sign up
    Returns a response
    """
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    return redirect(url_for('auth.login'))


class LoginForm(Form):
    """Form for login"""
    email_or_username = StringField(
        "Nombre de usuario o correo electrónico",
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Contraseña",
        validators=[InputRequired()]
    )


@auth.route("/login", methods=["POST"])
def login():
    """
    Renders a template for login
    Returns a string
    """
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("signup_post"))
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    """
    Returns a page to confirm user's login
    Returns a response
    """
    return redirect(url_for("index"))


@auth.route("/logout")
def logout():
    """
    Returns a page to confirm user logout
    Returns a response
    """
    return "Logout"
