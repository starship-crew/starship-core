from flask import Blueprint
from flask_restx import Api


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
api = Api(api_bp)
