import os

from .data import db_session

from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


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

    from .data.user import User

    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.login == "admin").first():
        admin_user = User()
        admin_user.login = "admin"
        admin_user.set_password(get_initial_admin_password())
        admin_user.is_admin = True
        db_sess.add(admin_user)
        db_sess.commit()


def make_app():
    from api.blueprint import api_bp
    from admin.blueprint import admin_bp

    app = Flask(__name__)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.config["SECRET_KEY"] = get_secret_key()

    db_session.global_init()
    login_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(admin_bp)
        app.register_blueprint(api_bp)

        create_inital_admin()

    print("Application was created successfully")

    return app
