"""Database models"""

import secrets
from datetime import date
import pyscrypt
from . import db


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(40), unique=True)
    salt = db.Column(db.String())
    password = db.Column(db.String)
    since_date = db.Column(db.Date)
    about = db.Column(db.String(256))
    avatar_id = db.Column(db.String(1))

    def __init__(self, name, email, password, about, avatar_id):
        self.name = name
        self.email = email
        self.salt = secrets.token_hex(8)
        self.password = pyscrypt.hash(password=password.encode(),
                                      salt=self.salt.encode(),
                                      N=2048,
                                      r=1,
                                      p=1,
                                      dkLen=256)
        self.avatar_id = avatar_id
        self.about = about
        self.since_date = date.today()
