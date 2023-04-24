from starship.data.action import Action, ActionKind
from starship.data.detail_copy import DetailCopy
from . import error
from starship.data import db
from starship.helpers import get_crew, get_lang
from .blueprint import api
from flask_restx import Resource, reqparse, inputs

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)
parser.add_argument("action", required=False)
parser.add_argument("part", required=False, type=inputs.natural)


@api.route("/combat")
class CombatResource(Resource):
    def get(self):
        args = parser.parse_args()

        with db.session() as db_sess:
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

            action_comment = (
                crew.action_comment.get(get_lang()) if crew.action_comment else None
            )

            return {
                "crew": opponent.as_response,
                "ship": opponent_ship,
                "actions": [action.as_response for action in crew.available_actions],
                "action_comment": action_comment,
                "won": crew.won,
            }

    def post(self):
        args = parser.parse_args()

        with db.session() as db_sess:
            if not args["action"]:
                return error.response("action_argument_not_provided")

            if not (crew := get_crew(db_sess, args["token"])):
                return error.response("crew_not_found")

            if crew.action is not None:
                return error.response("already_acted")

            try:
                kind = ActionKind[args["action"]]
            except KeyError:
                return error.response("action_argument_wrong")

            if (
                args["part"]
                and not db_sess.query(DetailCopy)
                .filter_by(id=args["part"], ship=crew.ship)
                .first()
            ):
                return error.response("part_not_found")

            crew.action = Action(kind=kind, part=args["part"])
            db_sess.commit()
            return crew.action.as_response
