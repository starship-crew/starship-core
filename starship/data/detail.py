import yaml
import sqlalchemy as sa
from starship.data.detail_copy import DetailCopy

from starship.helpers import get_lang

from .db_session import SqlAlchemyBase


class Detail(SqlAlchemyBase):
    __tablename__ = "details"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    kind_id = sa.Column(sa.Integer, sa.ForeignKey("detail_types.id"))
    kind = sa.orm.relationship("DetailType", foreign_keys=[kind_id])

    cost = sa.Column(sa.Integer, nullable=False)
    health = sa.Column(sa.Integer, nullable=False)

    power_generation = sa.Column(sa.Integer, default=0)
    power_consumption = sa.Column(sa.Integer, default=0)
    accel_factor = sa.Column(sa.Float, default=0.0)
    damage_absorption = sa.Column(sa.Integer, default=0)
    damage = sa.Column(sa.Integer, default=0)
    stability = sa.Column(sa.Float, default=0.0)
    mobility = sa.Column(sa.Float, default=0.0)
    detail_limit = sa.Column(sa.Integer, default=0)

    name_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    name = sa.orm.relationship("Sentence", foreign_keys=[name_id])

    description_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    description = sa.orm.relationship("Sentence", foreign_keys=[description_id])

    def __repr__(self):
        return f"Detail(id={self.id!r}, name={self.name!r}, description={self.description!r}, kind={self.kind!r}, cost={self.cost!r}, ...)"

    def chars_to_yaml(self):
        obj = {
            "power_generation": self.power_generation,
            "accel_factor": self.accel_factor,
            "damage_absorption": self.damage_absorption,
            "damage": self.damage,
            "stability": self.stability,
            "mobility": self.mobility,
        }
        return yaml.dump(obj, allow_unicode=True)

    @property
    def as_response(self):
        lang = get_lang()
        return {
            "id": self.id,
            "kind": self.kind.as_response,
            "name": self.name.get(lang),
            "description": self.description.get(lang),
            "cost": self.cost,
            "health": self.health,
            "power_generation": self.power_generation,
            "accel_factor": self.accel_factor,
            "damage_absorption": self.damage_absorption,
            "damage": self.damage,
            "stability": self.stability,
            "mobility": self.mobility,
            "detail_limit": self.detail_limit,
        }
