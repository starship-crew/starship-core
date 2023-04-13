from .blueprint import admin_bp

from flask_login import login_required
from flask import render_template, url_for, redirect


@admin_bp.errorhandler(403)
@login_required
def forbidden(e):
    return render_template("403.html", title=f"Forbidden")


@admin_bp.errorhandler(404)
def not_found(e):
    return redirect(url_for("admin_bp.dashboard"))
