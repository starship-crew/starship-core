import sqlalchemy as sa

from typing import List

from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy
from starship.data.detail_type import DetailType

from . import db
from .db import SqlAlchemyBase


class Ship(SqlAlchemyBase):
    __tablename__ = "ships"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    shame_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    shame = sa.orm.relationship(
        "Sentence",
        foreign_keys=[shame_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )

    enhanced_mobility = sa.Column(sa.Float, default=0.0)

    crew_id = sa.Column(sa.Integer, sa.ForeignKey("crews.id"))
    crew = sa.orm.relationship("Crew", back_populates="ship", foreign_keys=[crew_id])

    details: sa.orm.Mapped[List["DetailCopy"]] = sa.orm.relationship(
        back_populates="ship"
    )

    def __repr__(self):
        return f"Ship(id={self.id!r}, shame={self.shame!r}, crew={self.crew!r})"

    @property
    def health(self):
        return sum(map(lambda d: d.health, self.details))

    @property
    def damage_absorption(self) -> float:
        return sum(map(lambda d: d.kind.damage_absorption, self.details))

    @property
    def damage(self):
        return sum(map(lambda d: d.kind.damage, self.details))

    @property
    def stability(self) -> float:
        return sum(map(lambda d: d.kind.stability, self.details))

    @property
    def power_generation(self):
        return sum(map(lambda d: d.kind.power_generation, self.details))

    @property
    def power_consumption(self):
        return sum(map(lambda d: d.kind.power_consumption, self.details))

    @property
    def accel_factor(self) -> float:
        return sum(map(lambda d: d.kind.accel_factor, self.details))

    @property
    def detail_limit(self):
        return sum(map(lambda d: d.kind.detail_limit, self.details))

    @property
    def mobility(self) -> float:
        if self.enhanced_mobility == None:
            self.enhanced_mobility = 0.0
        return (
            sum(map(lambda d: d.kind.mobility, self.details)) + self.enhanced_mobility
        )

    @property
    def as_response(self):
        return {
            "shame": self.shame,
            "detail_copies": [dc.as_response for dc in self.details],
            "health": self.health,
            "mobility": self.mobility,
            "damage_absorption": self.damage_absorption,
            "damage": self.damage,
            "stability": self.stability,
            "power_generation": self.power_generation,
            "power_consumption": self.power_consumption,
            "accel_factor": self.accel_factor,
            "detail_limit": self.detail_limit,
        }

    def detail(self, detail_type_id):
        """Checks whether ship has a detail with the type provided and if it
        does, it returns its model"""

        with db.session() as db_sess:
            return (
                db_sess.query(DetailCopy)
                .filter_by(ship=self)
                .join(DetailCopy.kind)
                .join(Detail.kind)
                .filter(DetailType.id == detail_type_id)
                .first()
            )
