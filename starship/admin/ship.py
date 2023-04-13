from .blueprint import admin_bp
from .helpers import admin_required


@admin_bp.route("/create_ship")
@admin_required
def create_ship():
    return {}
