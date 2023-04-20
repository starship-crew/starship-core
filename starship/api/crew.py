import sqlalchemy as sa
import secrets

from starship.helpers import get_crew
from . import error
from starship.data import db_session
from starship.data.crew import Crew
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.data.garage import Garage
from starship.data.ship import Ship
from .blueprint import api
from flask_restx import Resource, reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument("name", required=True)

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)

CREW_TOKEN_LENGTH = 32


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

    db_sess.add(crew)
    db_sess.commit()

    return token


@api.route("/crew")
class CrewResource(Resource):
    def post(self):
        args = post_parser.parse_args()

        try:
            token = create_crew(args["name"])
            return {"token": token}, 201
        except sa.exc.IntegrityError:
            return error.response("crew_already_exists")

    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        return crew.as_response
