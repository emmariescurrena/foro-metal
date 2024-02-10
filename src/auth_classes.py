"""Froms for auth"""

from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired
from flask_wtf import FlaskForm


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
        default=""
    )


class CreateTopicForm(FlaskForm):
    """Form for create topic"""

    title = StringField(
        "Título del tópico",
        validators=[InputRequired(), Length(max=256)]
    )
    text = StringField(
        "Texto",
        validators=[InputRequired(), Length(max=10000)],
        widget=TextArea()
    )
    tags = StringField(
        "Etiquetas para ayudar a otros a encontrar tu tópico",
        render_kw={"placeholder": "Ej.: thrash-metal guitar black-sabbath"}
    )


class CreateReplyForm(FlaskForm):
    """Form for create reply"""

    text = StringField(
        "Respuesta",
        validators=[InputRequired(), Length(max=10000)],
        widget=TextArea()
    )
