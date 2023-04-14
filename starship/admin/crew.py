from starship import api
from flask import redirect
from .blueprint import admin_bp
from .helpers import admin_required, redirect_url


@admin_bp.route("/create_crew/<name>")
@admin_required
def create_crew(name):
    api.create_crew(name)
    return redirect(redirect_url())
