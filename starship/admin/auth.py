from starship.data.user import User
from starship.data import db
from .blueprint import admin_bp
from .forms.user import LoginForm
from .helpers import redirect_url
from starship import login_manager

from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_required, logout_user, login_user


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_bp.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        with db.session() as db_sess:
            user = db_sess.query(User).filter_by(login=form.login.data).first()

            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)

                return redirect(redirect_url("admin_bp.dashboard"))

        flash("Invalid login/password")

        return redirect(url_for("admin_bp.login"))

    return render_template("login.html", form=form, title="Dashboard Login")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_bp.login"))


@login_manager.user_loader
def load_user(user_id):
    with db.session() as db_sess:
        if user_id is not None:
            return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("admin_bp.login"))
