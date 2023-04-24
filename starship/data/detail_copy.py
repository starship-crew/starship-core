import sqlalchemy as sa

from starship.helpers import get_lang

from .db import SqlAlchemyBase


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

    @property
    def max_health(self):
        return self.kind.health

    @property
    def upgrade_cost(self):
        if (not_starter := int(self.kind.cost / 2 * self.level)) != 0:
            return not_starter
        return 10 * self.level

    @property
    def repair_cost(self):
        if self.health == self.max_health:
            return 0
        return self.upgrade_cost // 3

    @property
    def name(self):
        return self.kind.name

    @property
    def description(self):
        return self.kind.description

    @property
    def cost(self):
        return self.kind.cost

    @property
    def order(self):
        return self.kind.kind.order

    @property
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

    @property
    def crew(self):
        """Returns crew which owns this detail or None if it's orphan (has no
        linked crew's ship or one's garage)"""

        if self.ship:
            return self.ship.crew

        if self.garage:
            return self.garage.crew

    @property
    def power_generation(self):
        return self.kind.power_generation

    @property
    def power_consumption(self):
        return self.kind.power_consumption

    @property
    def accel_factor(self):
        return self.kind.accel_factor

    @property
    def damage_absorption(self):
        return self.kind.damage_absorption

    @property
    def damage(self):
        return self.kind.damage

    @property
    def stability(self):
        return self.kind.stability

    @property
    def mobility(self):
        return self.kind.mobility

    @property
    def detail_limit(self):
        return self.kind.detail_limit

    @property
    def as_response(self):
        lang = get_lang()
        return {
            "id": self.id,
            "name": self.name.get(lang),
            "description": self.description.get(lang),
            "type_id": self.kind.id,
            "kind": self.kind.kind.as_response,
            "health": self.health,
            "max_health": self.max_health,
            "order": self.order,
            "required": self.required,
            "level": self.level,
            "cost": self.cost,
            "upgrade_cost": self.upgrade_cost,
            "repair_cost": self.repair_cost,
            "power_generation": self.power_generation,
            "power_consumption": self.power_consumption,
            "accel_factor": self.accel_factor,
            "mobility": self.mobility,
            "stability": self.stability,
            "damage_absorption": self.damage_absorption,
            "damage": self.damage,
            "detail_limit": self.detail_limit,
        }
