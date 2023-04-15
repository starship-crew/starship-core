import yaml

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import (
    SelectField,
    BooleanField,
    IntegerField,
    SubmitField,
    TextAreaField,
)

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
    cost = IntegerField("Cost", default=0)
    health = IntegerField("Health", default=0)
    chars = TextAreaField(
        "Characteristics",
        validators=[YamlValidator()],
        default=DEFAULT_DETAIL_CHARS_TEXTAREA_VALUE,
    )
    submit = SubmitField("Create")
