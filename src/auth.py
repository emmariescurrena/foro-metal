"""Module to manage and verify user credentials"""

from flask import Blueprint, redirect, url_for, render_template, request, flash
from wtforms import StringField, PasswordField, RadioField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired
from flask_wtf import FlaskForm
from .models import User
from . import db


auth = Blueprint("auth", __name__)


class SignUpForm(FlaskForm):
    """Form for sign up"""
    name = StringField("Nombre de usuario*",
                       validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField("Correo electrónico*",
                        validators=[InputRequired(), Length(min=6, max=40)])
    password = PasswordField(
        "Contraseña*", validators=[InputRequired(), Length(min=8, max=72)])
    confirm = PasswordField("Confirmar contraseña*",
                            validators=[EqualTo("password")])
    avatar_id = RadioField("Choose avatar",
                           validators=[InputRequired()],
                           choices=["1", "2", "3"],
                           render_kw={"class": "input-hidden"})
    about = StringField("Frase que te describa",
                        validators=[Length(max=256)],
                        widget=TextArea())


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

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Correo electrónico ya registrado")
            return redirect(url_for("auth.signup"))

        new_user = User(name=name,
                        email=email,
                        password=password,
                        avatar_id=avatar_id,
                        about=about)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


class LoginForm(FlaskForm):
    """Form for login"""
    email_or_username = StringField(
        "Nombre de usuario o correo electrónico",
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Contraseña",
        validators=[InputRequired()]
    )


@auth.route("/login")
def login():
    """
    Renders a template for login
    Returns a string
    """

    form = LoginForm(request.form)
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    """
    Returns a page to confirm user's login
    Returns a response
    """

    return redirect(url_for("main.index"))


@auth.route("/logout")
def logout():
    """
    Returns a page to confirm user logout
    Returns a response
    """

    return "Logout"
