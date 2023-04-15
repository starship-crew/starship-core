from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import (
    SelectField,
    BooleanField,
    IntegerField,
    SubmitField,
    TextAreaField,
)

from starship.admin.helpers import YamlValidator


class DetailTypeCreationForm(FlaskForm):
    name = TextAreaField("Name", validators=[DataRequired(), YamlValidator()])
    description = TextAreaField("Description", validators=[YamlValidator()])
    required = BooleanField("Required by any ship to work", default=False)
    submit = SubmitField("Create")


DEFAULT_DETAIL_CHARS_TEXTAREA_VALUE = """power_generation: 0
power_consumption: 0
accel_factor: 0.0
damage_absorption: 0
damage: 0"""


class DetailCreationForm(FlaskForm):
    name = TextAreaField("Name", validators=[DataRequired(), YamlValidator()])
    description = TextAreaField("Description", validators=[YamlValidator()])
    kind = SelectField(
        "Type", validate_choice=False, coerce=int, validators=[DataRequired()]
    )
    cost = IntegerField("Cost (set to 0 to mark detail as a starter one)", default=0)
    health = IntegerField("Health", default=0)
    chars = TextAreaField(
        "Characteristics",
        validators=[YamlValidator()],
        default=DEFAULT_DETAIL_CHARS_TEXTAREA_VALUE,
    )
    submit = SubmitField("Create")
