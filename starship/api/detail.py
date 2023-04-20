from . import error
from starship.data import db_session
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.helpers import get_crew
from .blueprint import api
from flask_restx import Resource, reqparse, inputs

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)
parser.add_argument("id", required=True, type=inputs.natural)


@api.route("/detail")
class DetailResource(Resource):
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not (detail := db_sess.query(Detail).filter_by(id=args["id"]).first()):
            return error.response("detail_not_found")

        if crew.currency < detail.cost:
            return error.response("not_enough_currency")

        crew.currency -= detail.cost

        dc = DetailCopy.new(detail)
        dc.garage = crew.garage
        dc.garage.details.append(dc)

        db_sess.add(dc)
        db_sess.commit()

        return {
            "detail_id": args["id"],
            "detail_copy_id": dc.id,
            "garage_id": crew.garage.id,
        }
