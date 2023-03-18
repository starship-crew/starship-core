from models import Crew, User
from starship import login_manager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from flask import Blueprint, abort, flash, redirect, request, url_for, render_template
from starship import db

from starship.helper import is_safe_url

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/dashboard")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


@admin_bp.route("/")
@login_required
def dashboard():
    if not current_user.is_admin:
        return abort(403)
    return render_template(
        "admin/dashboard.html",
        title="Dashboard",
        users=db.session.query(User).all(),
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

            next = request.args.get("next")

            if not is_safe_url(next):
                abort(400)

            return redirect(next or url_for("admin_bp.dashboard"))

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
