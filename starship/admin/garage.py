from collections import OrderedDict
import sqlalchemy as sa

from flask import abort, flash, redirect, render_template
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.data.detail_type import DetailType
from starship.data.garage import Garage
from starship.data import db_session
from .blueprint import admin_bp
from .helpers import admin_required, get_lang, redirect_url


@admin_bp.route("/garage/<int:id>")
@admin_required
def garage(id):
    db_sess = db_session.create_session()
    garage = db_sess.query(Garage).get(id)

    if not garage:
        return abort(404)

    detail_types = db_sess.query(DetailType).order_by(DetailType.order).all()
    details = OrderedDict()
    for detail_type in detail_types:
        details[detail_type] = (
            db_sess.query(DetailCopy)
            .filter(DetailCopy.garage == garage)
            .join(DetailCopy.kind)
            .join(Detail.kind)
            .filter(DetailType.id == detail_type.id)
            .all()
        )

    return render_template(
        "garage.html",
        title=f"Garage {garage.id}",
        garage=garage,
        details=details,
        lang=get_lang(),
    )


@admin_bp.route("/garage/<int:id>/delete")
@admin_required
def delete_garage(id):
    db_sess = db_session.create_session()
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
