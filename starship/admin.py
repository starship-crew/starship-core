import sqlalchemy as sa

from sqlalchemy import desc
from models import Crew, User
from starship import login_manager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from flask import Blueprint, abort, flash, redirect, request, url_for, render_template
from starship import db
from functools import wraps
from starship.helper import is_safe_url

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/dashboard")


def redirect_url(default="admin_bp.dashboard"):
    next = request.args.get("next")
    if next and not is_safe_url(next):
        abort(400)
    return next or request.referrer or url_for(default)


@admin_bp.errorhandler(403)
@login_required
def forbidden(e):
    return render_template(
        "admin/user.html", title=f"User {current_user.login}", user=current_user
    )


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


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


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
        return db.session.query(User).get(user_id)
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


@admin_bp.route("/user/<int:user_id>")
@admin_required
def user(user_id):
    user = db.session.query(User).get(user_id)
    if not user:
        return abort(404)
    return render_template("admin/user.html", title=f"User {user.login}", user=user)


# @admin_bp.route("/user/<int:user_id>/set_currency/<new_currency>")
# @admin_required
# def set_user_currency(user_id, new_currency):
#     user = db.session.query(User).get(user_id)

#     if not user:
#         return redirect(redirect_url())

#     try:
#         user.currency = new_currency
#         db.session.commit()
#     except sa.exc.DataError as e:
#         flash(f"Error while changing user's currency value: {e}")

#     return redirect(redirect_url())


@admin_bp.route("/user/<int:id>/set_<field>/<value>")
def change_user_field(id, field, value):
    user = db.session.query(User).get(id)

    if not user:
        return redirect(redirect_url())

    try:
        match field:
            case "login":
                user.login = value
            case "password":
                user.password = value
            case "currency":
                user.currency = value
        db.session.commit()
    except sa.exc.IntegrityError:
        flash(f'User with {field} "{value}" already exists')
    except sa.exc.DataError:
        flash(f'Failed to change {field} to "{value}" cause of data processing issues')

    return redirect(redirect_url())


@admin_bp.route("/create_crew")
@admin_required
def create_crew():
    return {}


@admin_bp.route("/create_ship")
@admin_required
def create_ship():
    return {}
