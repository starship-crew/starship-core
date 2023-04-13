import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class RequiredShipDetail(SqlAlchemyBase):
    __tablename__ = "required_ship_details"

    id = sa.Column(sa.Integer, primary_key=True)
    detail_type_id = sa.Column(sa.Integer, sa.ForeignKey("detail_types.id"))
    detail_type = sa.orm.relationship("DetailType", foreign_keys=[detail_type_id])

    def __repr__(self):
        return f"ReuqiredShipDetail(id={self.id!r}, detail_type={self.detail_type!r}"
