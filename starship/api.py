from collections import OrderedDict
import secrets


from starship.data import db_session
from starship.data.crew import Crew
from starship.data.garage import Garage
from starship.data.ship import Ship
from starship.data.detail import Detail
from starship.data.detail_type import DetailType
from starship.data.detail_copy import DetailCopy

from flask import Blueprint, request

from starship.data.user import User
from starship.helpers import get_lang


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

CREW_TOKEN_LENGTH = 32

ERRORS = {
    "id_list_parse": {"en": "Could not convert provided user identifiers to integers"},
    "crew_not_found": {"en": "Could not find crew with provided token"},
    "ship_not_linked": {"en": "Could not find ship linked with provided crew"},
    "garage_not_linked": {"en": "Could not find garage linked with provided crew"},
    "dc_does_not_belong_to_crew": {
        "en": "Detail copy with provided id does not belong to provided crew"
    },
}


def error_response(error_id):
    return {"status": -1, "reason": ERRORS[error_id][get_lang()]}


def response(**kwargs):
    kwargs["status"] = 0
    return kwargs


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

    garage = Garage()

    crew = Crew()
    crew.token = token
    crew.name = name
    crew.ship = ship
    crew.garage = garage

    linked_users = set()
    if user_ids := request.args.get("linked_users", None):
        try:
            user_ids = set(map(int, user_ids.split(",")))
        except ValueError:
            return error_response("id_list_parse")
        for user in db_sess.query(User).filter(User.id.in_(user_ids)):
            crew.owners.add(user)
            linked_users.add(user.id)

    db_sess.add(crew)
    db_sess.commit()

    return {"status": 0, "token": token, "linked_users": linked_users}


def get_crew(db_sess, token):
    return db_sess.query(Crew).filter_by(token=token).first()


@api_bp.route("/crew/<token>")
def crew(token):
    db_sess = db_session.create_session()
    crew = db_sess.query(Crew).filter_by(token=token).first()

    if not crew:
        return error_response("crew_not_found")

    return crew.as_response


@api_bp.route("/crew/<token>/ship")
def ship(token):
    db_sess = db_session.create_session()

    if not (crew := get_crew(db_sess, token)):
        return error_response("crew_not_found")

    if not (ship := db_sess.query(Ship).filter_by(crew=crew).first()):
        return error_response("ship_not_linked")

    return ship.as_response


@api_bp.route("/store")
def store():
    lang = get_lang()
    db_sess = db_session.create_session()

    detail_types = db_sess.query(DetailType).order_by(DetailType.order).all()
    details = OrderedDict()

    for detail_type in detail_types:
        details[detail_type] = (
            db_sess.query(Detail)
            .filter_by(kind=detail_type)
            .order_by(Detail.cost)
            .all()
        )

    return {dt.as_response: d.as_response for dt, d in details.items()}


@api_bp.route("/crew/<token>/garage")
def garage(token):
    db_sess = db_session.create_session()

    if not (crew := get_crew(db_sess, token)):
        return error_response("crew_not_found")

    if not crew.garage:
        return error_response("garage_not_linked")

    return crew.garage.as_response


@api_bp.route("/crew/<token>/detail_copy/<int:id>/put_on")
def put_on(token, id):
    db_sess = db_session.create_session()

    if not (crew := get_crew(db_sess, token)):
        return error_response("crew_not_found")

    if not (dc := db_sess.query(DetailCopy).filter_by(id=id).first()):
        return error_response("dc_not_found")

    if dc.crew != crew:
        return error_response("dc_does_not_belong_to_crew")

    return dc.put_on()


@api_bp.route("/crew/<token>/detail_copy/<int:id>/put_off")
def put_off(token, id):
    db_sess = db_session.create_session()

    if not (crew := get_crew(db_sess, token)):
        return error_response("crew_not_found")

    if not (dc := db_sess.query(DetailCopy).filter_by(id=id).first()):
        return error_response("dc_not_found")

    if dc.crew != crew:
        return error_response("dc_does_not_belong_to_crew")

    return dc.put_off()
