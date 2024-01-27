"""Setup basic structure for app"""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
load_dotenv()


def create_app():
    """
    Creates app and set auth and main blueprints
    Returns app
    """

    app = Flask(__name__)

    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"

    db.init_app(app)

    # pylint: disable=import-outside-toplevel

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # pylint: enable=import-outside-toplevel

    return app
