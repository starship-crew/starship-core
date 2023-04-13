import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class DetailCopy(SqlAlchemyBase):
    __tablename__ = "details_copies"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    ship_id = sa.Column(sa.Integer, sa.ForeignKey("ships.id"))
    ship = sa.orm.relationship("Ship", foreign_keys=[ship_id])

    kind_id = sa.Column(sa.Integer, sa.ForeignKey("details.id"))
    kind = sa.orm.relationship("Detail", foreign_keys=[kind_id])

    level = sa.Column(sa.Integer, default=1)

    def __repr__(self):
        return f"DetailCopy(id={self.id!r}, ship={self.ship!r}, kind={self.kind!r}, level={self.level!r})"
