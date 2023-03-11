import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


def get_secret_key():
    with open(os.getenv("SECRET_KEY_FILE", "/run/secrets/secret_key")) as file:
        return file.read().rstrip()


def make_app():
    import dbhelper
    from api import api_bp
    from admin import admin_bp
    import models

    app = Flask(__name__)

    app.config["SECRET_KEY"] = get_secret_key()
    app.config["SQLALCHEMY_DATABASE_URI"] = dbhelper.get_url()

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(admin_bp)
        app.register_blueprint(api_bp)

        db.create_all()

    print("Application was created successfully")

    return app
