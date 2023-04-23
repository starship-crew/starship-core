import sqlalchemy as sa

from typing import Set
from .db_session import SqlAlchemyBase
from enum import Enum, auto


class Action(Enum):
    Attack = auto()
    Dodge = auto()
    FoolGiveUp = auto()
    SmartGiveUp = auto()
    SelfDestruct = auto()


class Crew(SqlAlchemyBase):
    __tablename__ = "crews"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    token = sa.Column(sa.String(255), unique=True)
    name = sa.Column(sa.String(255), unique=True)
    currency = sa.Column(sa.Integer, default=0)

    ship = sa.orm.relationship("Ship", uselist=False, back_populates="crew")
    garage = sa.orm.relationship("Garage", uselist=False, back_populates="crew")

    combat_id = sa.Column(sa.Integer, sa.ForeignKey("combats.id"))
    combat = sa.orm.relationship("Combat", back_populates="crews")
    active = sa.Column(sa.Boolean, default=False)

    searching = sa.Column(sa.Boolean, default=False)

    action = sa.Column(sa.Enum(Action))

    owners: sa.orm.Mapped[Set["User"]] = sa.orm.relationship(
        secondary="crew_groups",
        back_populates="crews",
    )

    def __repr__(self):
        return f"Crew(name={self.name!r}, currency={self.currency!r})"

    @property
    def as_response(self):
        return {"name": self.name, "currency": self.currency}
