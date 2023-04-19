from typing import OrderedDict
from starship.data import db_session
from starship.data.detail import Detail
from starship.data.detail_type import DetailType
from .blueprint import api
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("token", required=True)


@api.route("/store")
class StoreResource(Resource):
    def get(self):
        db_sess = db_session.create_session()

        detail_types = db_sess.query(DetailType).order_by(DetailType.order).all()
        details = OrderedDict()

        for detail_type in detail_types:
            details[detail_type] = (
                db_sess.query(Detail)
                .filter_by(kind=detail_type)
                .order_by(Detail.cost)
                .all()
            )

        return {dt.as_response: d.as_response for dt, d in details.items()}, 200
