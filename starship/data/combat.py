from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from starship.data.crew import Crew

from .db_session import SqlAlchemyBase


class Combat(SqlAlchemyBase):
    __tablename__ = "combats"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    crews: Mapped[List["Crew"]] = relationship(back_populates="combat")

    def __repr__(self):
        return f"Combat(crews={self.crews!r})"
