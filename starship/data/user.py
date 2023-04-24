import sqlalchemy as sa

from typing import Set
from flask_login import UserMixin
from .db import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    login = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String, unique=False)
    is_admin = sa.Column(sa.Boolean)
    crews: sa.orm.Mapped[Set["Crew"]] = sa.orm.relationship(secondary="crew_groups")

    def __repr__(self):
        return f"User(id={self.id}, login={self.login}, password={self.password}, admin={self.is_admin})"

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_primary_admin(self):
        return self.login == "admin" and self.is_admin
