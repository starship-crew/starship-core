import sqlalchemy as sa

from typing import List

from .db_session import SqlAlchemyBase


class Ship(SqlAlchemyBase):
    __tablename__ = "ships"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    shame = sa.Column(sa.String(255))

    crew_id = sa.Column(sa.Integer, sa.ForeignKey("crews.id"))
    crew = sa.orm.relationship("Crew", back_populates="ship", foreign_keys=[crew_id])

    details: sa.orm.Mapped[List["DetailCopy"]] = sa.orm.relationship(
        secondary="detail_copy_groups"
    )

    def __repr__(self):
        return f"Ship(id={self.id!r}, shame={self.shame!r}, crew={self.crew!r})"
