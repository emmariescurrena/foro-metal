"""Forms for auth"""

from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired
from flask_wtf import FlaskForm
from bcrypt import checkpw
from .auth_queries import get_user_with_email, get_user_with_name
from .signup_custom_validators import (NameRegistered,
                                       NameNotEmail,
                                       EmailRegistered,
                                       ValidEmailFormat,
                                       ValidEmailDns,
                                       ValidPasswordFormat,
                                       valid_email_format)


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
    avatar_id = RadioField("Elegir avatar",
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

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        name_or_email = self.name_or_email.data
        if valid_email_format(name_or_email):
            user = get_user_with_email(name_or_email)
            inexistent_user_message = "El correo electrónico no se encuentra registrado"
        else:
            user = get_user_with_name(name_or_email)
            inexistent_user_message = "El nombre de usuario no se encuentra registrado"

        if not user:
            self.name_or_email.errors.append(inexistent_user_message)
            return False

        hashed_password = user.password
        if not checkpw(self.password.data.encode("utf8"), hashed_password):
            self.name_or_email.errors.append("Contraseña incorrecta")
            return False

        self.user = user
        return True
