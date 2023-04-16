import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class DetailCopy(SqlAlchemyBase):
    __tablename__ = "details_copies"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    ship_id = sa.Column(sa.Integer, sa.ForeignKey("ships.id"))
    ship = sa.orm.relationship("Ship", foreign_keys=[ship_id])

    garage_id = sa.Column(sa.Integer, sa.ForeignKey("garages.id"))
    garage = sa.orm.relationship("Garage", foreign_keys=[garage_id])

    kind_id = sa.Column(sa.Integer, sa.ForeignKey("details.id"))
    kind = sa.orm.relationship("Detail", foreign_keys=[kind_id])

    health = sa.Column(sa.Integer, nullable=False)
    level = sa.Column(sa.Integer, default=1)

    def __repr__(self):
        return f"DetailCopy(id={self.id!r}, ship={self.ship!r}, kind={self.kind!r}, level={self.level!r})"

    def put_on(self):
        if self.garage:
            self.ship = self.garage.crew.ship
            self.garage = None

    def put_off(self):
        if self.ship:
            self.garage = self.ship.crew.garage
            self.ship = None

    def crew(self):
        """Returns crew which owns this detail or None if it's orphan (has no
        linked crew's ship or one's garage)"""

        if self.ship:
            return self.ship.crew

        if self.garage:
            return self.garage.crew
