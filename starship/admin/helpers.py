from flask import request
from functools import wraps
from urllib.parse import urljoin, urlparse

from flask import abort, url_for
from flask_login import login_required, current_user


def is_safe_url(target):
    """A function that ensures that a redirect target will lead to the same server."""

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def redirect_url(default="admin_bp.dashboard"):
    next = request.args.get("next")
    if next and not is_safe_url(next):
        abort(400)
    return next or request.referrer or url_for(default)


def admin_required(func):
    @wraps(func)
    @login_required
    def new_func(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return func(*args, **kwargs)

    return new_func
