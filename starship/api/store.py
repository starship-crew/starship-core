from starship.data import db_session
from starship.helpers import get_detail_types, get_ordered_details
from .blueprint import api
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)


@api.route("/store")
class StoreResource(Resource):
    def get(self):
        db_sess = db_session.create_session()

        return {
            "detail_types": [dt.as_response for dt in get_detail_types(db_sess)],
            "details": {
                dt.id: [detail.as_response for detail in details]
                for dt, details in get_ordered_details(db_sess).items()
            },
        }
