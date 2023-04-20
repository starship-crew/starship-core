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
            req = db_sess.query(Crew).filter(
                Crew.searching,
                Crew.currency.between(crew.currency * 0.5, crew.currency * 1.5),
            )
            while len(req.count()) == 0:
                pass
            enemy = req.first()

            combat = Combat()
            combat.active = crew
            crew.combat = combat

            crew.searching = False

        db_sess.commit()

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")
