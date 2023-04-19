from . import error
from starship.data import db_session
from starship.data.ship import Ship
from starship.helpers import get_crew
from .blueprint import api
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)


@api.route("/ship")
class ShipResource(Resource):
    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not (ship := db_sess.query(Ship).filter_by(crew=crew).first()):
            return error.response("ship_not_linked")

        return ship.as_response
