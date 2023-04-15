from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField

from starship.admin.helpers import YamlValidator


class ShipShameEditionForm(FlaskForm):
    shame = TextAreaField("Shame", validators=[YamlValidator()])
    submit = SubmitField("Edit")
