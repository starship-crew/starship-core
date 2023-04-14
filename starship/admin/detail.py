import yaml
import sqlalchemy as sa

from starship.data import db_session
from .blueprint import admin_bp
from .helpers import admin_required, redirect_url
from starship.data.sentence import Sentence
from starship.data.detail_type import DetailType
from starship.data.detail import Detail
from .forms.detail import DetailTypeCreationForm

try:
    from yaml import CBaseLoader as YamlLoader
except ImportError:
    from yaml import BaseLoader as YamlLoader

from flask import flash, redirect, render_template, request, url_for

# Default language
LANG = "ru"


def get_lang():
    return request.args.get("lang", LANG)


@admin_bp.route("/details")
@admin_required
def detail_management():
    db_sess = db_session.create_session()

    detail_types = db_sess.query(DetailType).all()
    details = {}
    for detail_type in detail_types:
        details[detail_type] = (
            db_sess.query(Detail)
            .filter_by(kind=detail_type)
            .order_by(Detail.cost)
            .all()
        )

    return render_template(
        "details.html",
        title="Detail Management",
        details_page=True,
        lang=get_lang(),
        detail_types=db_sess.query(DetailType).all(),
        details=details,
    )


def yaml_to_sentence(text, sentence=None):
    """YAML text to the Sentence.
    For example, string
    "en: ABC
    ru: АБВ"
    will be converted to Sentence(en="ABC", ru="АБВ")."""

    if not sentence:
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
        detail_type.required = form.required.data
        db_sess.add(detail_type)
        db_sess.commit()
        return redirect(url_for("admin_bp.detail_management"))

    return render_template(
        "create_detail_type.html",
        form=form,
        title="Detail Type creation",
        details_page=True,
    )


@admin_bp.route("/detail_type/<int:id>")
@admin_required
def detail_type(id):
    db_sess = db_session.create_session()
    dt = db_sess.query(DetailType).get(id)
    if not dt:
        flash(f"Detail type with id {id} not found")
        return redirect(redirect_url())
    return render_template(
        "detail_type.html",
        title=dt.name.en,
        lang=get_lang(),
        dt=dt,
        details_page=True,
    )


@admin_bp.route("/detail_type/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def edit_detail_type(id):
    db_sess = db_session.create_session()
    dt = db_sess.query(DetailType).get(id)

    if not dt:
        flash(f"Detail type with id {id} not found")
        return redirect(redirect_url())

    form = DetailTypeCreationForm()

    if form.validate_on_submit():
        dt.name = yaml_to_sentence(form.name.data, dt.name)
        dt.description = (
            yaml_to_sentence(form.description.data, dt.description)
            if form.description.data
            else Sentence()
        )
        dt.required = form.required.data
        db_sess.commit()
        return redirect(url_for("admin_bp.detail_type", id=id))

    return render_template(
        "edit_detail_type.html",
        title="Edit Detail Type",
        form=form,
        dt=dt,
        details_page=True,
    )


@admin_bp.route("/detail_type/<int:id>/delete")
@admin_required
def delete_detail_type(id):
    db_sess = db_session.create_session()
    dt = db_sess.query(DetailType).get(id)

    if not dt:
        flash(f"Detail type with id {id} not found")
        return redirect(redirect_url())

    try:
        db_sess.delete(dt)
        db_sess.commit()
    except sa.exc.SQLAlchemyError as e:
        flash(f"Error while deleting detail_type with id {id}: {e}")

    return redirect(url_for("admin_bp.detail_management"))
