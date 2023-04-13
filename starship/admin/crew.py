from .blueprint import admin_bp
from .helpers import admin_required


@admin_bp.route("/create_crew")
@admin_required
def create_crew():
    return {}
