"""Forms for auth"""

from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired
from flask_wtf import FlaskForm
from .custom_validators import (NameRegistered, NameNotEmail, EmailRegistered,
                                ValidEmailFormat, ValidEmailDns, ValidPasswordFormat)


# pylint: disable=no-value-for-parameter
class SignUpForm(FlaskForm):
    """Form for sign up"""
    name = StringField("Nombre de usuario*",
                       validators=[
                           InputRequired(),
                           Length(min=4, max=30),
                           NameRegistered(),
                           NameNotEmail()
                       ])
    email = StringField("Correo electrónico*",
                        validators=[
                            InputRequired(),
                            Length(min=6, max=40),
                            EmailRegistered(),
                            ValidEmailFormat(),
                            ValidEmailDns()
                        ])
    password = PasswordField("Contraseña*",
                             validators=[
                                 InputRequired(),
                                 Length(min=8, max=72),
                                 ValidPasswordFormat(),
                                 EqualTo("confirm")])
    confirm = PasswordField("Confirmar contraseña*")
    avatar_id = RadioField("Choose avatar",
                           validators=[InputRequired()],
                           choices=["1", "2", "3"],
                           render_kw={"class": "input-hidden"})
    about = StringField("Frase que te describa",
                        validators=[Length(max=256)],
                        widget=TextArea())


class LoginForm(FlaskForm):
    """Form for login"""
    name_or_email = StringField(
        "Nombre de usuario o correo electrónico",
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Contraseña",
        validators=[InputRequired()]
    )
    remember = BooleanField(
        "Recordarme",
        default=False
    )
