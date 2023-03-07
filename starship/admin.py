from flask import Blueprint

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/dashboard")


@admin_bp.route("/")
def admin():
    return {"status": "ok"}
