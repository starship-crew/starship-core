from typing import List
import sqlalchemy as sa

from starship.data.crew import Crew

from .db_session import SqlAlchemyBase


class Combat(SqlAlchemyBase):
    __tablename__ = "combats"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    crews: sa.orm.Mapped[List["Crew"]] = sa.orm.relationship(secondary="combat_groups")
    active = sa.Column(sa.Integer)

    def __repr__(self):
        return f"Combat(active={self.active_id!r}, passive={self.passive_id!r})"
