import yaml

from starship.data import db_session
from .blueprint import admin_bp
from .helpers import admin_required
from starship.data.sentence import Sentence
from starship.data.detail_type import DetailType
from .forms.detail import DetailTypeCreationForm

try:
    from yaml import CBaseLoader as YamlLoader
except ImportError:
    from yaml import BaseLoader as YamlLoader

from flask import redirect, render_template, request, url_for


@admin_bp.route("/details")
def detail_management():
    db_sess = db_session.create_session()
    lang = request.args.get("lang", "ru")
    return render_template(
        "details.html",
        title="Detail Management",
        details_page=True,
        lang=lang,
        detail_types=db_sess.query(DetailType).all(),
    )


def yaml_to_sentence(text):
    """YAML text to the Sentence.
    For example, string
    "en: ABC
    ru: АБВ"
    will be converted to Sentence(en="ABC", ru="АБВ")."""

    sentence = Sentence()

    pyobj = yaml.load(text, YamlLoader).items()

    for lang, value in pyobj:
        sentence.__setattr__(lang, value)

    return sentence


@admin_bp.route("/create_detail_type", methods=["GET", "POST"])
@admin_required
def create_detail_type():
    form = DetailTypeCreationForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        detail_type = DetailType()
        detail_type.name = yaml_to_sentence(form.name.data)
        detail_type.description = (
            yaml_to_sentence(form.description.data)
            if form.description.data
            else Sentence()
        )
        db_sess.add(detail_type)
        db_sess.commit()
        return redirect(url_for("admin_bp.detail_management"))

    return render_template(
        "create_detail_type.html",
        form=form,
        title="Detail Type creation",
        details_page=True,
    )
