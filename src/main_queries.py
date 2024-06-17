"""Main queries"""

from sqlalchemy import select
from .models import Topic, User, Reply, Tag, TopicTag, title_to_url
from . import db


def get_topics_for_index_page():
    """Get topics for index page"""

    result = (
        db.session.query(
            Topic.id,
            Topic.title,
            Topic.url,
            Topic.text,
            User.name.label("user_name"),
            Topic.date,
            db.func.array_agg(Tag.name).label("tags")
        )
        .outerjoin(TopicTag, Topic.id == TopicTag.id_topic)
        .outerjoin(Tag, TopicTag.id_tag == Tag.id)
        .outerjoin(User, Topic.id_user == User.id)
        .group_by(Topic.id, Topic.title, Topic.url, Topic.text, User.name, Topic.date)
        .order_by(Topic.id.desc())
        .all()
    )

    return result


def get_topic_for_topic_page(url):
    """
    Get required data from db to load a topic's page main topic
    Returns a sql.Row instance
    """

    info_topic = (
        db.session.query(
            Topic.title,
            Topic.text,
            User.avatar_id,
            User.name.label("user_name"),
            Topic.date,
            User.about.label("user_about"),
            Topic.id
        )
        .join(User)
        .filter(Topic.url == url)
        .one()
    )

    return info_topic


def get_replies_for_topic_page(id_topic):
    """
    Get required data from db to load a topic's page replies
    Returns a list
    """

    stmt = (
        select(
            Reply.text,
            User.avatar_id,
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


def topic_title_in_table(title):
    """Returns True if topic name in table, else False"""

    url = title_to_url(title)
    return True if Topic.query.filter_by(url=url).first() else False


def tag_in_table(name):
    """Returns True if tag in table, else False"""

    return True if Tag.query.filter_by(name=name).first() else False


def adds_tag_not_present_in_table(tag):
    """Adds tag if it is not present on the table"""

    if not tag_in_table(tag.name):
        db.session.add(tag)


def add_session_tags(tags):
    """Adds tags to session"""

    for tag in tags:
        adds_tag_not_present_in_table(tag)


def get_id_tags(tags):
    """Get id of multiple tags"""

    id_tags = []
    for tag in tags:
        tag_id = (db.session.query(Tag.id).filter(Tag.name == tag.name))
        id_tags.append(tag_id)
    return id_tags


def insert_topic_tag_db(id_topic, id_tags):
    """Insert id topic and id tag in topic-tag table"""

    for id_tag in id_tags:
        topic_tag = TopicTag(id_topic=id_topic,
                             id_tag=id_tag)
        db.session.add(topic_tag)
    db.session.commit()


def get_topic_url_with_id(id_topic):
    """Get url of topic with given id"""

    result = db.session.query(Topic.url).filter(Topic.id == id_topic).one()
    url = result[0]
    return url


def get_tagged_topics(tag_name):
    """Get topics with respective tag"""

    result = (
        db.session.query(
            Topic.id,
            Topic.title,
            Topic.url,
            Topic.text,
            User.name.label("user_name"),
            Topic.date,
            db.func.array_agg(Tag.name).label("tags")
        )
        .outerjoin(TopicTag, Topic.id == TopicTag.id_topic)
        .outerjoin(Tag, TopicTag.id_tag == Tag.id)
        .outerjoin(User, Topic.id_user == User.id)
        .filter(Tag.name == tag_name)
        .group_by(Topic.id, Topic.title, Topic.url, Topic.text, User.name, Topic.date)
        .order_by(Topic.id.desc())
        .all()
    )

    return result
