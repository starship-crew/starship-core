import sqlalchemy as sa

from typing import List

from .db_session import SqlAlchemyBase


class Garage(SqlAlchemyBase):
    __tablename__ = "garages"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    crew_id = sa.Column(sa.Integer, sa.ForeignKey("crews.id"))
    crew = sa.orm.relationship("Crew", back_populates="garage", foreign_keys=[crew_id])

    details: sa.orm.Mapped[List["DetailCopy"]] = sa.orm.relationship(
        secondary="garage_groups"
    )

    def __repr__(self):
        return f"Garage(id={self.id!r}, details={self.details})"
