import secrets


from starship.data import db_session
from starship.data.crew import Crew
from starship.data.ship import Ship
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy

from flask import Blueprint, request

from starship.data.user import User


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

    starter_details = db_sess.query(Detail).filter_by(cost=0)
    for detail in starter_details:
        detail_copy = DetailCopy()
        detail_copy.ship = ship
        detail_copy.kind = detail
        detail_copy.health = detail.health
        ship.details.append(detail_copy)

    crew = Crew()
    crew.token = token
    crew.name = name
    crew.ship = ship

    linked_users = set()
    if user_ids := request.args.get("linked_users", None):
        try:
            user_ids = set(map(int, user_ids.split(",")))
        except ValueError:
            return {
                "status": -1,
                "reason": "Could not convert provided user identifiers to integers",
            }
        for user in db_sess.query(User).filter(User.id.in_(user_ids)):
            crew.owners.add(user)
            linked_users.add(user.id)

    db_sess.add(crew)
    db_sess.commit()

    return {"status": 0, "token": token, "linked_users": linked_users}
