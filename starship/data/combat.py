from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from starship.data.crew import Crew

from .db import SqlAlchemyBase


class Combat(SqlAlchemyBase):
    __tablename__ = "combats"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    crews: Mapped[List["Crew"]] = relationship(back_populates="combat")

    def __repr__(self):
        return f"Combat(crews={self.crews!r})"

    def opponent_for(self, crew) -> Crew | None:
        """Returns opponent's crew for the provided one or None, if there's
        not."""

        if not self.crews:
            return None

        for combat_crew in self.crews:
            if combat_crew != crew:
                return combat_crew
