"""Database models"""

from secrets import token_hex
from datetime import date
from typing import Optional
import pyscrypt
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db


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


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40))
    salt: Mapped[str] = mapped_column(String(16))
    password: Mapped[str] = mapped_column(String)
    since_date: Mapped[date]
    about: Mapped[Optional[str]] = mapped_column(String(256))
    avatar_id: Mapped[int]

    def __init__(self, name, email, password, about, avatar_id):
        self.name = name
        self.email = email
        self.salt = token_hex(8)
        self.password = pyscrypt.hash(password=password.encode(),
                                      salt=self.salt.encode(),
                                      N=2048,
                                      r=1,
                                      p=1,
                                      dkLen=256)
        self.avatar_id = int(avatar_id)
        self.about = about
        self.since_date = date.today()


class Topic(db.Model):
    """Topic model"""

    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column(String(10000))
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date]
    url: Mapped[str] = mapped_column(String(1000))

    user = relationship("User", foreign_keys="Topic.id_user")

    def __init__(self, name, text, id_user):
        self.name = name
        self.text = text
        self.id_user = id_user
        self.date = date.today()
        self.url = title_to_url(name)


class Reply(db.Model):
    """Reply model"""

    __tablename__ = "replies"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_topic: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    text: Mapped[str] = mapped_column(String(10000))
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date]

    topic = relationship("Topic", foreign_keys="Reply.id_topic")
    user = relationship("User", foreign_keys="Reply.id_user")

    def __init__(self, id_topic, text, id_user):
        self.id_topic = id_topic
        self.text = text
        self.id_user = id_user
        self.date = date.today()
