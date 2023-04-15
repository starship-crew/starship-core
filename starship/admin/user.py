import sqlalchemy as sa

from starship.data.user import User
from starship.data import db_session
from .blueprint import admin_bp
from .helpers import redirect_url
from .helpers import admin_required
from .forms.user import UserCreationForm

from flask_login import current_user
from flask import redirect, url_for, render_template, abort, flash


@admin_bp.route("/create_user", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserCreationForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        exists = db_sess.query(User).filter_by(login=form.login.data).first()
        if not exists:
            user = User()
            user.login = form.login.data
            user.set_password(form.password.data)
            user.is_admin = form.is_admin.data

            db_sess.add(user)
            db_sess.commit()

            return redirect(url_for("admin_bp.dashboard"))

        flash("User with this login already exists")

    return render_template("create_user.html", form=form, title="User creation")


@admin_bp.route("/user/<int:id>")
@admin_required
def user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return abort(404)
    return render_template("user.html", title=f"User {user.login}", user=user)


@admin_bp.route("/user/<int:id>/toggle_admin")
@admin_required
def toggle_admin_state(id):
    if current_user.id == id:
        flash(f"Removing admin rights from the currently joined user is disallowed")
        return redirect(redirect_url())

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    if user.is_primary_admin():
        flash(f"Removing admin rights from the primary admin is disallowed")
        return redirect(redirect_url())

    user.is_admin = not user.is_admin
    db_sess.commit()

    return redirect(redirect_url("admin_bp.dashboard"))


@admin_bp.route("/user/<int:id>/set_<field>/<value>")
@admin_required
def change_user_field(id, field, value):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    if not user:
        flash(f"User with id {id} not found")
        return redirect(redirect_url())

    if user.is_primary_admin() and field == "login":
        flash(f"Can't change login of primary admin")
        return redirect(redirect_url())

    try:
        match field:
            case "login":
                user.login = value
            case "password":
                user.set_password(value)
        db_sess.commit()
    except sa.exc.IntegrityError:
        flash(f'User with {field} "{value}" already exists')
    except sa.exc.DataError:
        flash(f'Failed to change {field} to "{value}" cause of data processing issues')

    return redirect(redirect_url())


@admin_bp.route("/user/<int:id>/delete")
@admin_required
def delete_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    if not user:
        flash(f"User with id {id} not found")
        return redirect(redirect_url())

    if user.is_primary_admin():
        flash(f"Can't delete primary admin")
        return redirect(redirect_url())

    try:
        db_sess.delete(user)
        db_sess.commit()
    except sa.exc.SQLAlchemyError as e:
        flash(f"Error while deleting user with id {id}: {e}")

    return redirect(redirect_url())
