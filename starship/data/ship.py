import sqlalchemy as sa

from typing import List

from .db_session import SqlAlchemyBase


class Ship(SqlAlchemyBase):
    __tablename__ = "ships"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    shame_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    shame = sa.orm.relationship("Sentence", foreign_keys=[shame_id])

    crew_id = sa.Column(sa.Integer, sa.ForeignKey("crews.id"))
    crew = sa.orm.relationship("Crew", back_populates="ship", foreign_keys=[crew_id])

    details: sa.orm.Mapped[List["DetailCopy"]] = sa.orm.relationship(
        secondary="detail_copy_groups"
    )

    def __repr__(self):
        return f"Ship(id={self.id!r}, shame={self.shame!r}, crew={self.crew!r})"

    @property
    def health(self):
        return sum(map(lambda d: d.health, self.details))

    @property
    def damage_absorption(self) -> float:
        return sum(map(lambda d: d.damage_absorption, self.details))

    @property
    def damage(self):
        return sum(map(lambda d: d.damage, self.details))

    @property
    def stability(self) -> float:
        return sum(map(lambda d: d.stability, self.details))

    @property
    def power_generation(self):
        return sum(map(lambda d: d.power_generation, self.details))

    @property
    def power_consumption(self):
        return sum(map(lambda d: d.power_consumption, self.details))

    @property
    def accel_factor(self) -> float:
        return sum(map(lambda d: d.accel_factor, self.details))

    @property
    def detail_limit(self):
        return sum(map(lambda d: d.detail_limit, self.details))

    @property
    def mobility(self) -> float:
        return sum(map(lambda d: d.detail_limit, self.details))

    @property
    def as_response(self):
        return {
            "shame": self.shame,
            "detail_copies": [dc.as_response() for dc in self.details],
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
