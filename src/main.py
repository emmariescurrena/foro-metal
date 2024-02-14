"""Topicos and usuario pages"""

from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from .models import Topic
from .main_classes import CreateTopicForm, CreateReplyForm
from .main_queries import (get_topics_for_index_page,
                           get_topic_for_topic_page,
                           get_replies_for_topic_page,
                           get_user_for_user_page,
                           insert_topic_db,
                           insert_tags_db)


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


@main.route("/topicos/<url>")
def topic(url=None):
    """
    Renders template for topico
    Returns a string
    """

    info_topic = get_topic_for_topic_page(url)
    id_topic = info_topic.id
    replies = get_replies_for_topic_page(id_topic)
    form = CreateReplyForm(request.form)

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


@main.route("/crear-topico")
@login_required
def create_topic():
    """
    Renders template for create topic
    Returns a string
    """

    form = CreateTopicForm(request.form)
    if form.validate_on_submit():

        name = request.form.get("name")
        text = request.form.get("text")
        id_user = current_user.get_id()
        tags = request.form.get("tags").split()

        info_topic = Topic(name=name,
                           text=text,
                           id_user=id_user)

        insert_topic_db(info_topic)
        insert_tags_db(tags)
        insert_topic_tag_db(topic_tag_arr):

    return render_template("crear_topico.html", form=form)
