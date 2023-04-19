import secrets
from . import error
from starship.data import db_session
from starship.data.crew import Crew
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.data.garage import Garage
from starship.data.ship import Ship
from starship.data.user import User
from .blueprint import api
from flask_restx import Resource, reqparse, inputs

post_parser = reqparse.RequestParser()
post_parser.add_argument("name", required=True)
post_parser.add_argument("linked_users", type=inputs.natural, action="split")

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)

CREW_TOKEN_LENGTH = 32


@api.route("/crew")
class CrewResource(Resource):
    def post(self):
        args = post_parser.parse_args()
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
        crew.name = args["name"]
        crew.ship = ship
        crew.garage = garage

        linked_users = set()
        if user_ids := args.get("linked_users", None):
            for user in db_sess.query(User).filter(User.id.in_(user_ids)):
                crew.owners.add(user)
                linked_users.add(user.id)

        db_sess.add(crew)
        db_sess.commit()

        return {"token": token}, 201

    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        crew = db_sess.query(Crew).filter_by(token=args["token"]).first()

        if not crew:
            return error.response("crew_not_found")

        return crew.as_response
