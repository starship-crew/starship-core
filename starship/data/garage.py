from collections import OrderedDict
import sqlalchemy as sa

from typing import List
from starship.data.detail import Detail
from starship.data.detail_copy import DetailCopy

from starship.data.detail_type import DetailType

from .db_session import SqlAlchemyBase, create_session


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
        db_sess = create_session()

        detail_types = db_sess.query(DetailType).order_by(DetailType.order).all()
        details = OrderedDict()

        for detail_type in detail_types:
            details[detail_type] = (
                db_sess.query(DetailCopy)
                .filter(DetailCopy.garage == self)
                .join(DetailCopy.kind)
                .join(Detail.kind)
                .filter(DetailType.id == detail_type.id)
                .all()
            )

        return details

    @property
    def as_response(self):
        return {dt.as_response: d.as_response for dt, d in self.ordered_details.items()}
