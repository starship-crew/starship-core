import sqlalchemy as sa

from flask import abort, flash, redirect, render_template, url_for
from starship.admin.forms.ship import ShipShameEditionForm
from starship.data.ship import Ship
from starship.data import db_session
from .blueprint import admin_bp
from .helpers import admin_required, get_lang, redirect_url, yaml_to_sentence


@admin_bp.route("/ship/<int:id>")
@admin_required
def ship(id):
    db_sess = db_session.create_session()
    ship = db_sess.query(Ship).get(id)
    if not ship:
        return abort(404)
    return render_template(
        "ship.html",
        title=f"Ship {ship.id}",
        ship=ship,
        details=sorted(ship.details, key=lambda d: d.kind.kind.order),
        lang=get_lang(),
    )


@admin_bp.route("/ship/<int:id>/change_shame", methods=["GET", "POST"])
@admin_required
def change_ship_shame(id):
    db_sess = db_session.create_session()
    ship = db_sess.query(Ship).get(id)

    if not ship:
        flash(f"Ship with id {id} not found")
        return redirect(redirect_url())

    form = ShipShameEditionForm()

    if form.validate_on_submit():
        ship.shame = yaml_to_sentence(form.shame.data, ship.shame)
        db_sess.commit()
        return redirect(url_for("admin_bp.ship", id=id))

    return render_template(
        "edit_ship_shame.html",
        title="Edit Shame",
        form=form,
        ship=ship,
    )


@admin_bp.route("/ship/<int:id>/delete")
@admin_required
def delete_ship(id):
    db_sess = db_session.create_session()
    ship = db_sess.query(Ship).get(id)

    if not ship:
        flash(f"Ship with id {id} not found")
        return redirect(redirect_url())

    try:
        db_sess.delete(ship)
        db_sess.commit()
    except sa.exc.SQLAlchemyError as e:
        flash(f"Error while deleting ship with id {id}: {e}")

    return redirect(redirect_url())
