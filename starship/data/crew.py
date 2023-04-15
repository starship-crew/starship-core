import sqlalchemy as sa

from typing import Set
from .db_session import SqlAlchemyBase


class Crew(SqlAlchemyBase):
    __tablename__ = "crews"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    token = sa.Column(sa.String(255), unique=True)
    name = sa.Column(sa.String(255), unique=True)

    ship = sa.orm.relationship("Ship", uselist=False, back_populates="crew")

    owners: sa.orm.Mapped[Set["User"]] = sa.orm.relationship(
        secondary="crew_groups",
        back_populates="crews",
    )

    def __repr__(self):
        return f"Crew(name={self.name!r}, ship={self.ship!r}, token={self.token!r}, owner={self.owner!r})"
