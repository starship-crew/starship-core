from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")


class UserCreationForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    is_admin = BooleanField("Admin", default=False)
    submit = SubmitField("Create")
