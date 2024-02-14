"""Auth queries"""

from .models import User
from . import db


def get_user_with_email(email):
    """Get user data with email given"""

    return User.query.filter_by(email=email).first()


def get_user_with_name(name):
    """Get user data with name given"""

    return User.query.filter_by(name=name).first()


def insert_user_db(user):
    """Inserts new user in users table"""

    db.session.add(user)
    db.session.commit()
