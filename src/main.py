"""Topicos and usuario pages"""

from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for, render_template
from sqlalchemy import select
from .models import Topic, User, Reply
from . import db

main = Blueprint("main", __name__)
load_dotenv()


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

    stmt = (
        select(
            Topic.name,
            Topic.url,
            Topic.text,
            Topic.date,
            User.name.label("user_name")
        )
        .join(User)
    )
    result = db.session.execute(stmt)
    topics = result.all()

    return render_template("index.html", topics=topics)


def get_db_topic_page_topic(url):
    """
    Get required data from db to load a topic's page main topic
    Returns a sql.Row instance
    """

    stmt = (
        select(
            Topic.name,
            Topic.text,
            User.name.label("user_name"),
            Topic.date,
            User.about.label("user_about"),
            Topic.id
        )
        .join(User)
        .filter(Topic.url == url)
    )
    result = db.session.execute(stmt)
    info_topic = result.one()

    return info_topic


def get_db_topic_page_replies(id_topic):
    """
    Get required data from db to load a topic's page replies
    Returns a list
    """

    stmt = (
        select(
            Reply.text,
            User.name.label("user_name"),
            Reply.date,
            User.about.label("user_about")
        )
        .join(User)
        .filter(Reply.id_topic == id_topic)
    )
    result = db.session.execute(stmt)
    replies = result.all()

    return replies


@main.route("/topicos/<url>")
def topic(url=None):
    """
    Renders template for topico
    Returns a string
    """

    info_topic = get_db_topic_page_topic(url)
    id_topic = info_topic.id
    replies = get_db_topic_page_replies(id_topic)

    return render_template("topico.html", info_topic=info_topic, replies=replies)


def get_db_user_page(username):
    """
    Get required data from db to load a user page
    Returns a list
    """

    stmt = (
        select(
            User.name,
            User.avatar_id,
            User.since_date,
            User.about,
        )
        .filter(User.name == username)
    )
    result = db.session.execute(stmt)
    info_user = result.one()

    return info_user


@main.route("/usuario/<username>")
def user(username=None):
    """
    Renders and returns template for usuario
    Returns a string
    """

    info_user = get_db_user_page(username)
    return render_template("usuario.html", info_user=info_user)
