import sqlalchemy as sa

from flask import abort, flash, redirect, render_template
from starship.data.garage import Garage
from starship.data import db
from .blueprint import admin_bp
from .helpers import admin_required, redirect_url
from starship.helpers import get_lang


@admin_bp.route("/garage/<int:id>")
@admin_required
def garage(id):
    with db.session() as db_sess:
        garage = db_sess.query(Garage).get(id)

        if not garage:
            return abort(404)

        return render_template(
            "garage.html",
            title=f"Garage {garage.id}",
            garage=garage,
            lang=get_lang(),
        )


@admin_bp.route("/garage/<int:id>/delete")
@admin_required
def delete_garage(id):
    with db.session() as db_sess:
        garage = db_sess.query(Garage).get(id)

        if not garage:
            flash(f"Garage with id {id} not found")
            return redirect(redirect_url())

        try:
            db_sess.delete(garage)
            db_sess.commit()
        except sa.exc.SQLAlchemyError as e:
            flash(f"Error while deleting garage with id {id}: {e}")

    return redirect(redirect_url())
