# Default language
from flask import request


LANG = "en"


def get_lang():
    return request.args.get("lang", LANG)
