import yaml

from flask import request
from functools import wraps
from urllib.parse import urljoin, urlparse

from flask import abort, url_for
from wtforms.validators import ValidationError
from flask_login import login_required, current_user

from starship.data.sentence import Sentence

# try using fast LibYAML C library for parsing yaml and falling back to pure
# Python implementation
try:
    from yaml import CBaseLoader as YamlLoader
except ImportError:
    from yaml import BaseLoader as YamlLoader


class YamlValidator:
    def __init__(self, message=None):
        if not message:
            message = "Field doesn't contain valid YAML formatted text."
        self.message = message

    def __call__(self, form, field):
        try:
            if len(field.data) != 0 and ":" not in field.data:
                raise yaml.YAMLError
            yaml.load(field.data, YamlLoader)
        except yaml.YAMLError:
            raise ValidationError(self.message)


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


def yaml_to_sentence(text, sentence=None):
    if not sentence:
        sentence = Sentence()

    try:
        pyobj = yaml.load(text, YamlLoader).items()

        for lang, value in pyobj:
            sentence.__setattr__(lang, value)
    except AttributeError:
        pass

    return sentence
