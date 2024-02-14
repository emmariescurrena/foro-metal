"""Main queries"""

from sqlalchemy import select
from .models import Topic, User, Reply
from . import db


def get_topics_for_index_page():
    """Get topics for index page"""

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

    return topics


def get_topic_for_topic_page(url):
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


def get_replies_for_topic_page(id_topic):
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


def get_user_for_user_page(username):
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


def insert_topic_db(info_topic):
    """Insert topic in db"""

    db.session.add(info_topic)
    db.session.commit()


def insert_tags_db(tags):
    """Insert tags in tags table"""

    for tag in tags:
        db.session.add(tag)
    db.session.commit()


def insert_topic_tag_db(topics_tags):
    """Insert id topic and id tag in topic-tag table"""

    for topic_tag in topics_tags:
        db.session.add(topic_tag)
    db.session.commit()
