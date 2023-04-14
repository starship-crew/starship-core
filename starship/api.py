import secrets


from starship.data import db_session
from starship.data.crew import Crew
from starship.data.ship import Ship
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy

from flask import Blueprint


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

CREW_TOKEN_LENGTH = 32


@api_bp.route("/")
def api():
    return {"status": 0}


@api_bp.route("/create_crew/<name>")
def create_crew(name):
    token = secrets.token_urlsafe(CREW_TOKEN_LENGTH)
    db_sess = db_session.create_session()

    ship = Ship()

    starter_details = db_sess.query(Detail).filter_by(cost=0).all()
    for detail in starter_details:
        detail_copy = DetailCopy()
        detail_copy.ship = ship
        detail_copy.kind = detail

    crew = Crew()
    crew.token = token
    crew.name = name
    crew.ship = ship

    db_sess.add(crew)
    db_sess.commit()

    return {"status": 0, "token": token}
