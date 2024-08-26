"""Setup basic structure for app"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from .models import Base

db = SQLAlchemy(model_class=Base)

def create_app():
    """
    Creates app and set auth and main blueprints
    Returns app
    """

    app = Flask(__name__)
    app.config.from_object("config")

    path = os.environ['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(path, echo=True)
    db.metadata.create_all(engine)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id_user):
        return User.query.get(int(id_user))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # pylint: enable=import-outside-toplevel

    return app
