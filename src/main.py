"""Topicos and usuario pages"""

from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from .models import Topic, Tag, Reply
from .main_classes import CreateTopicForm, CreateReplyForm
from .main_queries import (get_topics_for_index_page,
                           get_topic_for_topic_page,
                           get_replies_for_topic_page,
                           get_user_for_user_page,
                           add_session_tags,
                           get_id_tags,
                           insert_topic_tag_db,
                           get_topic_url_with_id,
                           get_tagged_topics)
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

    topics = get_topics_for_index_page()
    return render_template("index.html", topics=topics)


@main.route("/topicos/<url>", methods=["GET", "POST"])
def topic(url=None):
    """
    Renders template for topico
    Returns a string
    """

    info_topic = get_topic_for_topic_page(url)
    id_topic = info_topic.id
    replies = get_replies_for_topic_page(id_topic)
    form = CreateReplyForm(request.form)
    if form.validate_on_submit():

        text = form.text.data
        id_user = current_user.get_id()
        reply = Reply(id_topic=id_topic,
                      text=text,
                      id_user=id_user)
        db.session.add(reply)
        db.session.commit()

        return redirect(url_for("main.topic", url=url))

    return render_template("topico.html",
                           info_topic=info_topic,
                           replies=replies,
                           form=form)


@main.route("/perfil")
@login_required
def profile():
    """
    Renders template for perfil
    Returns a string
    """

    return render_template("perfil.html", name=current_user.name)


@main.route("/usuario/<username>")
def user(username=None):
    """
    Renders template for usuario
    Returns a string
    """

    info_user = get_user_for_user_page(username)
    return render_template("usuario.html", info_user=info_user)


def get_tags_array_from_tags_string(string):
    """Returns an array of Tag instances subtracted from a string"""

    tags = []
    for tag_name in string.split():
        tag = Tag(name=tag_name)
        tags.append(tag)

    return tags


@main.route("/crear-topico", methods=["GET", "POST"])
@login_required
def create_topic():
    """
    Renders template for create topic
    Returns a string
    """

    form = CreateTopicForm(request.form)
    if form.validate_on_submit():

        title = form.title.data
        text = form.text.data
        id_user = current_user.get_id()
        info_topic = Topic(title=title,
                           text=text,
                           id_user=id_user)
        db.session.add(info_topic)

        tags = get_tags_array_from_tags_string(form.tags.data)
        add_session_tags(tags)

        db.session.commit()

        id_topic = info_topic.id
        id_tags = get_id_tags(tags)
        insert_topic_tag_db(id_topic, id_tags)

        url = get_topic_url_with_id(id_topic)
        print(url)
        return redirect(url_for("main.topic", url=url))

    return render_template("crear_topico.html", form=form)


@main.route("/tagged/<tag_name>")
def tagged(tag_name=None):
    """
    Renders template for tagged topics
    Returns a string
    """

    topics = get_tagged_topics(tag_name)
    return render_template("tagged.html", tag_name=tag_name, topics=topics)
