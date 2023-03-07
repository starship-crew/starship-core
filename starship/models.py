from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from starship import db


class Crew(db.Model):
    __tablename__ = "crews"

    token = Column(String(255), primary_key=True)
    name = Column(String(255), unique=True)
    ship = Column(Integer, ForeignKey("ships.id"))

    Ship = relationship("Ship")


class Ship(db.Model):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True)
    shame = Column(String(255))


class DetailCopy(db.Model):
    __tablename__ = "details_copies"

    id = Column(Integer, primary_key=True)
    ship = Column(Integer, ForeignKey("ships.id"))
    kind = Column(Integer, ForeignKey("details.id"))

    ship = relationship("Ship")
    detail = relationship("Detail")


class Detail(db.Model):
    __tablename__ = "detalis"

    id = Column(Integer, primary_key=True)
    kind = Column(Integer, ForeignKey("details_types.id"))
    cost = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)
    power_generation = Column(Integer)
    accel_factor = Column(Float)
    damage_absorption = Column(Integer)
    damage = Column(Integer)
    name = Column(Integer, ForeignKey("senteces.id"))
    description = Column(Integer, ForeignKey("sentences.id"))

    details_types = relationship("DetailType")
    sentences = relationship("Sentence")


class DetailType(db.Model):
    __tablename__ = "detail_types"

    id = Column(Integer, primary_key=True)
    name = Column(Integer, ForeignKey("sentences.id"))
    description = Column(Integer, ForeignKey("sentences.id"))

    sentences = relationship("Sentence")


class Sentence(db.Model):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True)
    en = Column(String(6500))
    ru = Column(String(6500))


class RequiredShipDetail(db.Model):
    __tablename__ = "required_ship_details"

    detail_types = Column(Integer, ForeignKey("detail_types.id"), primary_key=True)

    detail_types_ref = relationship("DetailType")
