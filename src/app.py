"""Foro de metal app"""

import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request
from wtforms import Form, StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import Length, EqualTo, InputRequired

app = Flask(__name__)
load_dotenv()


def title_to_url(title):
    """
    Simplifies the topic's name to be saved as an url
    Returns a string
    """
    url = ""
    title = title.rstrip().lstrip()
    for char in title:
        if char in "aeiouáéíóúbcdfghjklmnñpqrstvwxyz":
            url += char
        elif char in "AEIOUÁÉÍÓÚBCDFGHJKLMNÑPQRSTVWXYZ":
            url += char.lower()
        elif char == " " and url[-1] != "-":
            url += "-"
    return url


def get_db_connection():
    """
    Get connection to 'foro_de_metal' database
    Returns an object
    """
    conn = psycopg2.connect(
        host="localhost",
        database="foro_de_metal",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn


@app.route("/")
def root():
    """
    Redirects from root to index
    Returns a response
    """
    return redirect(url_for('index'))


@app.route("/topicos")
def index():
    """
    Connects to DB and renders and returns template for index
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """SELECT top.url, top.name, top.text, us.name, top.date FROM topics top
    INNER JOIN users us ON top.id_user = us.id;"""
    cur.execute(sql)
    topics = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", topics=topics)


@app.route("/topicos/<url>")
def topic(url=None):
    """
    Connects to DB and renders and returns template for topico
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"""SELECT top.name, top.text, us.name, top.date, us.about, top.id FROM
    topics top INNER JOIN users us ON top.id_user = us.id WHERE top.url = '{url}';"""
    cur.execute(sql)
    info_topic = cur.fetchone()
    id_topic = info_topic[5]

    sql = f"""SELECT re.text, us.name, re.date, us.about FROM replies re INNER
    JOIN users us ON re.id_user = us.id WHERE re.id_topic = '{id_topic}';"""
    cur.execute(sql)
    replies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("topico.html", info_topic=info_topic, replies=replies)


@app.route("/usuario/<username>")
def user(username=None):
    """
    Connects to DB and renders and template for usuario
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"""SELECT name, img_id, since_date, about, topics_created,
    replies_writed FROM users WHERE name = '{username}';"""
    cur.execute(sql)
    info_user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("usuario.html", info_user=info_user)


class RegistrationForm(Form):
    """Form for register"""
    user = StringField(
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders and returns template for register
    Returns a string
    """

    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("registered"))
    return render_template("register.html", form=form)


@app.route("/registered")
def registered():
    """
    Renders a page to confirm user's register
    Returns a string
    """
    return "<p>Registered sucessfully</p>"


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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders a template for login
    Returns a string
    """
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("logged"))
    return render_template("login.html", form=form)


@app.route("/logged")
def logged():
    """
    Returns a page to confirm user's login
    Returns a string
    """
    return "<p>Logged sucessfully</p>"


if __name__ == '__main__':
    app.run(debug='DEBUG')
