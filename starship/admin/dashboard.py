from starship.data.ship import Ship
from starship.data.user import User
from starship.data.crew import Crew
from starship.data import db
from .blueprint import admin_bp
from .helpers import admin_required

from sqlalchemy import desc
from flask import render_template


@admin_bp.route("/")
@admin_required
def dashboard():
    with db.session() as db_sess:
        return render_template(
            "dashboard.html",
            title="Dashboard",
            users=db_sess.query(User).order_by(desc(User.is_admin)).all(),
            crews=db_sess.query(Crew).all(),
            ships=db_sess.query(Ship).all(),
        )
