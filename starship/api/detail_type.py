from . import error
from starship.data import db_session
from starship.data.detail_type import DetailType
from starship.helpers import get_crew, get_detail_types, get_lang
from .blueprint import api
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)
parser.add_argument("id", required=False, type=str)
parser.add_argument("key", required=False, type=str, default="none")


@api.route("/detail_type")
class DetailTypeResource(Resource):
    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if not (args["id"] or args["string_id"]):
            return error.response("dt_not_found")

        if not (dt := db_sess.query(DetailType).filter_by(id=args["id"]).first()):
            return error.response("dt_not_found")

        return dt.as_response


def convert_key(dt, key):
    try:
        attr = dt.__getattribute__(key)

        try:
            if attr.__tablename__ == "sentences":
                return attr.get(get_lang())
        except AttributeError:
            pass

        return attr
    except AttributeError:
        return error.response("dt_key_attr_error")


@api.route("/detail_types")
class DetailTypeListResource(Resource):
    def get(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()

        if not (crew := get_crew(db_sess, args["token"])):
            return error.response("crew_not_found")

        if args["key"] == "none":
            return [dt.as_response for dt in get_detail_types(db_sess)]

        return {
            convert_key(dt, args["key"]): dt.as_response
            for dt in get_detail_types(db_sess)
        }
