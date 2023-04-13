from starship.data.user import User
from starship.data.crew import Crew
from starship.data import db_session
from .blueprint import admin_bp
from .helpers import admin_required

from sqlalchemy import desc
from flask import render_template


@admin_bp.route("/")
@admin_required
def dashboard():
    db_sess = db_session.create_session()
    return render_template(
        "dashboard.html",
        title="Dashboard",
        users=db_sess.query(User).order_by(desc(User.is_admin)).all(),
        crews=db_sess.query(Crew).all(),
    )
