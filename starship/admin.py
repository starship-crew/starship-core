from sqlalchemy import desc
from models import Crew, User
from starship import login_manager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from flask import Blueprint, abort, flash, redirect, url_for, render_template
from starship import db
from starship.helper import redirect_url
from functools import wraps

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/dashboard")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


def admin_required(func):
    @wraps(func)
    @login_required
    def new_func(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return func(*args, **kwargs)

    return new_func


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        title="Dashboard",
        users=db.session.query(User).order_by(desc(User.is_admin)).all(),
        crews=db.session.query(Crew).all(),
    )


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_bp.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            return redirect(redirect_url("admin_bp.dashboard"))

        flash("Invalid login/password")

        return redirect(url_for("admin_bp.login"))

    return render_template("admin/login.html", form=form, title="Dashboard Login")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_bp.login"))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("admin_bp.login"))


@admin_bp.route("/toggle_admin_state/<int:user_id>")
@admin_required
def toggle_admin_state(user_id):
    if current_user.id != user_id:
        user = db.session.query(User).get(user_id)
        user.is_admin = not user.is_admin
        db.session.commit()
    return redirect(redirect_url("admin_bp.dashboard"))


class UserCreationForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    currency = IntegerField("Initial currency", default=0)
    is_admin = BooleanField("Admin", default=False)
    submit = SubmitField("Create")


@admin_bp.route("/create_user", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserCreationForm()

    if form.validate_on_submit():
        exists = db.session.query(User).filter_by(login=form.login.data).first()
        if not exists:
            user = User()
            user.login = form.login.data
            user.set_password(form.password.data)
            user.currency = form.currency.data
            user.is_admin = form.is_admin.data

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("admin_bp.dashboard"))

        flash("User with this login already exists")

    return render_template("admin/create_user.html", form=form, title="User creation")


@admin_bp.route("/create_crew")
@admin_required
def create_crew():
    return {}


@admin_bp.route("/create_ship")
@admin_required
def create_ship():
    return {}
