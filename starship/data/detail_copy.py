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

    @classmethod
    def new(cls, kind):
        return DetailCopy(kind=kind, health=kind.health)

    def name(self):
        return self.kind.name

    def description(self):
        return self.kind.description

    def cost(self):
        return self.kind.cost

    def order(self):
        return self.kind.kind.order

    def required(self):
        return self.kind.kind.required

    def can_put_on(self):
        return self.garage is not None

    def can_put_off(self):
        return self.ship is not None

    def put_on(self):
        if self.garage:
            self.ship = self.garage.crew.ship

            # If there's a detail with the same type as this, it must be put off
            # from the ship before putting on
            if dc := next(
                filter(lambda dc: dc.kind.kind == self.kind.kind, self.ship.details),
                None,
            ):
                dc.put_off()

            self.ship.details.append(self)
            self.garage.details.remove(self)
            self.garage = None

    def put_off(self):
        if self.ship:
            self.garage = self.ship.crew.garage
            self.garage.details.append(self)
            self.ship.details.remove(self)
            self.ship = None

    def crew(self):
        """Returns crew which owns this detail or None if it's orphan (has no
        linked crew's ship or one's garage)"""

        if self.ship:
            return self.ship.crew

        if self.garage:
            return self.garage.crew
