from starship.data.combat import Combat
from starship.data.crew import Crew
from . import error
from starship.data import db_session
from starship.helpers import get_crew
from .blueprint import api
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)


@api.route("/combat")
class CombatResource(Resource):
    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not crew.combat:
            crew.searching = True
            db_sess.commit()
            return {"action": "searching"}

        opponent = crew.opponent
        opponent_ship = (
            opponent.ship.as_response if crew.ship.detail("sensors") else None
        )

        return {
            "crew": opponent.as_response,
            "ship": opponent_ship,
            "actions": [action.as_response for action in crew.available_actions],
        }

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")
