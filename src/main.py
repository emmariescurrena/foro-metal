"""Topicos and usuario pages"""

import os
import psycopg2
from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for, render_template
from . import db

main = Blueprint("main", __name__)
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


@main.route("/")
def root():
    """
    Redirects from root to index
    Returns a response
    """
    return redirect(url_for('main.index'))


@main.route("/topicos")
def index():
    """
    Connects to DB and renders and returns template for index
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """SELECT
                top.url, top.name, top.text, us.name, top.date
            FROM
                topics top
            INNER JOIN
                users us
            ON
                top.id_user = us.id;"""
    cur.execute(sql)
    topics = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", topics=topics)


@main.route("/topicos/<url>")
def topic(url=None):
    """
    Connects to DB and renders and returns template for topico
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"""SELECT
                top.name, top.text, us.name, top.date, us.about, top.id
            FROM
                topics top
            INNER JOIN
                users us
            ON
                top.id_user = us.id
            WHERE
                top.url = '{url}';"""
    cur.execute(sql)
    info_topic = cur.fetchone()
    id_topic = info_topic[5]

    sql = f"""SELECT
                re.text, us.name, re.date, us.about
            FROM
                replies re
            INNER JOIN
                users us
            ON
                re.id_user = us.id
            WHERE
                re.id_topic = '{id_topic}';"""
    cur.execute(sql)
    replies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("topico.html", info_topic=info_topic, replies=replies)


@main.route("/usuario/<username>")
def user(username=None):
    """
    Connects to DB and renders and template for usuario
    Returns a string
    """
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"""SELECT
                name, img_id, since_date, about, topics_created, replies_writed
            FROM
                users
            WHERE
                name = '{username}';"""
    cur.execute(sql)
    info_user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("usuario.html", info_user=info_user)
