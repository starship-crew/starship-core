from . import error
from starship.data import db
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.helpers import get_crew, get_ordered_details
from .blueprint import api
from flask_restx import Resource, reqparse, inputs

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)
parser.add_argument("id", required=False, type=inputs.natural)


@api.route("/detail")
class DetailResource(Resource):
    def get(self):
        args = parser.parse_args()

        with db.session() as db_sess:
            if not (crew := get_crew(db_sess, args["token"])):
                return error.response("crew_not_found")

            if not (
                args["id"]
                and (detail := db_sess.query(Detail).filter_by(id=args["id"]).first())
            ):
                return error.response("detail_not_found")

            return detail.as_response

    def post(self):
        args = parser.parse_args()

        with db.session() as db_sess:
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


@api.route("/details")
class DetailDictResource(Resource):
    def get(self):
        args = parser.parse_args()

        with db.session() as db_sess:
            if not (crew := get_crew(db_sess, args["token"])):
                return error.response("crew_not_found")

            return {
                dt.id: [d.as_response for d in details]
                for dt, details in get_ordered_details(db_sess).items()
            }
