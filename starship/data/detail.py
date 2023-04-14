import yaml
import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class Detail(SqlAlchemyBase):
    __tablename__ = "details"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    kind_id = sa.Column(sa.Integer, sa.ForeignKey("detail_types.id"))
    kind = sa.orm.relationship("DetailType", foreign_keys=[kind_id])

    cost = sa.Column(sa.Integer, nullable=False)
    health = sa.Column(sa.Integer, nullable=False)

    power_generation = sa.Column(sa.Integer)
    accel_factor = sa.Column(sa.Float)
    damage_absorption = sa.Column(sa.Integer)
    damage = sa.Column(sa.Integer)

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
        }
        return yaml.dump(obj, allow_unicode=True)
