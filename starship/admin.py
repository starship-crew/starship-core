import requests

from models import User
from starship import login_manager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import current_user, login_user
from wtforms import PasswordField, StringField, SubmitField
from flask import Blueprint, flash, redirect, url_for, render_template

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/dashboard")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


@admin_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html", title="Dashboard")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_bp.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = requests.args.get("next")
            return redirect(next_page or url_for("admin_bp.dashboard"))

        flash("Invalid login/password")

        return redirect(url_for("admin_bp.login"))

    return render_template("admin/login.html", form=form, title="Dashboard Login")


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("admin_bp.login"))
