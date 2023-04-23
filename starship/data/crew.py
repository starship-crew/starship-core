import sqlalchemy as sa

from typing import List, Set
from typing_extensions import Self
from .db_session import SqlAlchemyBase
from enum import Enum, auto


class Action(Enum):
    Attack = auto()
    Dodge = auto()
    FoolGiveUp = auto()
    SmartGiveUp = auto()
    SelfDestruct = auto()

    def as_response(self):
        return self.name


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

    @property
    def opponent(self) -> Self | None:
        """Returns crew's opponent, if there's one."""
        if not self.combat:
            return None
        return self.combat.opponent_for(self)

    @property
    def available_actions(self) -> List[Action]:
        if not self.active or not self.ship:
            return []

        actions = []

        if self.ship.detail("weapon"):
            actions.append(Action.Attack)

        actions.append(Action.Dodge)

        if self.ship.detail("void_shields"):
            actions.append(Action.FoolGiveUp)

        if self.ship.detail("warp_engine"):
            actions.append(Action.SmartGiveUp)

        if self.ship.detail("plasma_generator"):
            actions.append(Action.SelfDestruct)
