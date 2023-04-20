from starship.helpers import get_lang
from .blueprint import api

ERRORS = {
    "crew_not_found": {
        "code": 404,
        "en": "Could not find crew with provided token",
        "ru": "Экипаж с заданным токеном не найден",
    },
    "ship_not_linked": {
        "code": 404,
        "en": "Could not find ship linked with provided crew",
        "ru": "Корабль привязанный к экипажу с данным токеном не найден",
    },
    "garage_not_linked": {
        "code": 404,
        "en": "Could not find garage linked with provided crew",
        "ru": "Гараж привязанный к эпипажу с данным токеном не найден",
    },
    "dc_does_not_belong_to_crew": {
        "code": 403,
        "en": "Detail copy with provided id does not belong to provided crew",
        "ru": "Экземпляр детали с данным id не принадлежит экипажу с данным токеном",
    },
    "not_enough_currency": {
        "code": 405,
        "en": "Insufficient funds (Qk) for the transaction",
        "ru": "Недостаточно средств (Qk) для проведения транзакции",
    },
    "crew_already_exists": {
        "code": 409,
        "en": "Crew with this name already exists",
        "ru": "Экипаж с данным именем уже существует",
    },
    "action_argument_not_provided": {
        "code": 400,
        "en": "action query argument was not provided",
        "ru": "action query-аргумент не был предоставлен",
    },
    "action_argument_wrong": {
        "code": 400,
        "en": "Wrong value of action query argument",
        "ru": "Неправильное значение action query-аргумента",
    },
    "detail_not_found": {
        "code": 404,
        "en": "Could not find detail with provided id",
        "ru": "Деталь с заданным id не найдена",
    },
}


def response(error_id):
    return api.abort(
        ERRORS[error_id]["code"], message=ERRORS[error_id][get_lang()], id=error_id
    )
