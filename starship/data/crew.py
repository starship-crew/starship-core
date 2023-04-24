import sqlalchemy as sa

from typing import List, Set
from typing_extensions import Self

from starship.data.action import ActionKind
from .db import SqlAlchemyBase


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

    action_id = sa.Column(sa.Integer, sa.ForeignKey("actions.id"))
    action = sa.orm.relationship("Action", back_populates="crew")

    action_comment_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    action_comment = sa.orm.relationship(
        "Sentence",
        foreign_keys=[action_comment_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )

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
    def won(self) -> bool | None:
        """Returns whether crew has won the combat."""
        if not self.combat or (self.ship.health > 0 and self.opponent.ship.health > 0):
            return None
        return self.opponent.ship.health <= 0

    @property
    def available_actions(self) -> List[ActionKind]:
        if not self.active or not self.ship:
            return []

        if self.won is not None:
            return [ActionKind.Quit]

        actions = []

        if self.ship.detail("weapon"):
            actions.append(ActionKind.Attack)

        actions.append(ActionKind.Dodge)

        if self.ship.detail("void_shields"):
            actions.append(ActionKind.FoolGiveUp)

        if self.ship.detail("warp_engine"):
            actions.append(ActionKind.SmartGiveUp)

        if self.ship.detail("plasma_generator"):
            actions.append(ActionKind.SelfDestruct)

        return actions
