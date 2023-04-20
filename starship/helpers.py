# Default language
from collections import OrderedDict
from flask import request

from starship.data.crew import Crew


LANG = "ru"


def get_lang():
    return request.args.get("lang", LANG)


def get_crew(db_sess, token):
    return db_sess.query(Crew).filter_by(token=token).first()


def get_detail_types(db_sess):
    from starship.data.detail_type import DetailType

    return db_sess.query(DetailType).order_by(DetailType.order).all()


def _get_ordered_details_inner(db_sess, detail_instance, query_applies=lambda q, dt: q):
    detail_types = get_detail_types(db_sess)
    details = OrderedDict()

    for detail_type in detail_types:
        details[detail_type] = query_applies(
            db_sess.query(detail_instance), detail_type
        ).all()

    return details


def get_ordered_details(db_sess, query_wrapper=lambda q, dt: q):
    from starship.data.detail import Detail

    return _get_ordered_details_inner(
        db_sess,
        Detail,
        lambda q, dt: query_wrapper(q.filter_by(kind=dt).order_by(Detail.cost), dt),
    )


def get_ordered_detail_copies(db_sess, query_wrapper=lambda q, dt: q):
    from starship.data.detail import Detail
    from starship.data.detail_type import DetailType
    from starship.data.detail_copy import DetailCopy

    return _get_ordered_details_inner(
        db_sess,
        DetailCopy,
        lambda q, dt: query_wrapper(
            q.join(DetailCopy.kind).join(Detail.kind).filter(DetailType.id == dt.id), dt
        ),
    )
