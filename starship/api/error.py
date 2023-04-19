from starship.helpers import get_lang
from .blueprint import api

ERRORS = {
    "crew_not_found": {
        "code": 404,
        "en": "Could not find crew with provided token",
    },
    "ship_not_linked": {
        "code": 404,
        "en": "Could not find ship linked with provided crew",
    },
    "garage_not_linked": {
        "code": 404,
        "en": "Could not find garage linked with provided crew",
    },
    "dc_does_not_belong_to_crew": {
        "code": 403,
        "en": "Detail copy with provided id does not belong to provided crew",
    },
    "not_enough_currency": {
        "code": 405,
        "en": "Insufficient funds for the transaction",
    },
}


def response(error_id):
    return api.abort(ERRORS[error_id]["code"], message=ERRORS[error_id][get_lang()])
