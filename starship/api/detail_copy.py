from . import error
from starship.data import db_session
from starship.data.detail_copy import DetailCopy
from starship.helpers import get_crew
from .blueprint import api
from flask_restx import Resource, reqparse, inputs

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)
parser.add_argument("id", required=True, type=inputs.natural)
parser.add_argument("action")


@api.route("/detail_copy")
class DetailCopyResource(Resource):
    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not (dc := db_sess.query(DetailCopy).filter_by(id=args["id"]).first()):
            return error.response("dc_not_found")

        if dc.crew != crew:
            return error.response("dc_does_not_belong_to_crew")

        return dc.as_response, 200

    def put(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not (dc := db_sess.query(DetailCopy).filter_by(id=args["id"]).first()):
            return error.response("dc_not_found")

        if dc.crew != crew:
            return error.response("dc_does_not_belong_to_crew")

        match action := args.get("action", None):
            case None:
                return error.response("action_argument_not_provided")
            case "put_on":
                dc.put_on()
            case "put_off":
                dc.put_off()
            case "upgrade":
                if dc.crew.currency < dc.upgrade_cost:
                    return error.response("not_enough_currency")

                dc.crew.currency -= dc.upgrade_cost
                dc.level += 1
            case "repair":
                if dc.crew.currency < dc.repair_cost:
                    return error.response("not_enough_currency")

                dc.crew.currency -= dc.repair_cost
                dc.health = dc.max_health
            case _:
                return error.response("action_argument_wrong")

        db_sess.commit()

        return {
            "detail_copy_id": args["id"],
            "action": action,
        }
