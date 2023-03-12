import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()

import models


def get_secret_key():
    with open(os.getenv("SECRET_KEY_FILE", "/run/secrets/secret_key")) as file:
        return file.read().rstrip()


def create_inital_admin():
    def get_initial_admin_password():
        FILE = os.getenv(
            "ADMIN_INITIAL_PASSWORD_FILE", "/run/secrets/admin_initial_password"
        )

        with open(FILE) as file:
            return file.read().rstrip()

    if (
        not db.session.query(models.User)
        .filter(models.User.login == "admin", models.User.is_admin)
        .first()
    ):
        admin_user = models.User()
        admin_user.login = "admin"
        admin_user.set_password(get_initial_admin_password())
        admin_user.is_admin = True
        db.session.add(admin_user)
        db.session.commit()


def make_app():
    import helper
    from api import api_bp
    from admin import admin_bp

    app = Flask(__name__)

    app.config["SECRET_KEY"] = get_secret_key()
    app.config["SQLALCHEMY_DATABASE_URI"] = helper.get_db_url()

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(admin_bp)
        app.register_blueprint(api_bp)

        db.create_all()

        create_inital_admin()

    print("Application was created successfully")

    return app
