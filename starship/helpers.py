# Default language
from flask import request

from starship.data.crew import Crew


LANG = "ru"


def get_lang():
    return request.args.get("lang", LANG)


def get_crew(db_sess, token):
    return db_sess.query(Crew).filter_by(token=token).first()
