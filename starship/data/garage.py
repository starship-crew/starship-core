import sqlalchemy as sa

from typing import List
from collections import OrderedDict
from starship.data.detail_copy import DetailCopy

from starship.data.detail_type import DetailType
from starship.helpers import get_ordered_detail_copies

from . import db_session
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

    @property
    def ordered_details(self) -> OrderedDict[DetailType, DetailCopy]:
        return get_ordered_detail_copies(
            db_session.create_session(),
            lambda q, dt: q.filter(DetailCopy.garage == self),
        )

    @property
    def as_response(self):
        return {
            "detail_types": [dt.as_response for dt in self.ordered_details.keys()],
            "details": {
                dt.string_id: [detail.as_response for detail in details]
                for dt, details in self.ordered_details.items()
            },
        }
