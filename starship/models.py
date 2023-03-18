from typing import List
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import Mapped, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from starship import db

crew_groups = Table(
    "crew_groups",
    db.metadata,
    Column("crew_id", ForeignKey("crews.id")),
    Column("user_id", ForeignKey("users.id")),
)

detail_copy_groups = Table(
    "detail_copy_groups",
    db.metadata,
    Column("detail_id", ForeignKey("details_copies.id")),
    Column("ship_id", ForeignKey("ships.id")),
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String, unique=False)
    currency = Column(Integer, default=0)
    is_admin = Column(Boolean)
    crews: Mapped[List["Crew"]] = relationship(secondary="crew_groups")

    def __repr__(self):
        return f"User(id={self.id}, login={self.login}, password={self.password}, admin={self.admin})"

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Sentence(db.Model):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    en = Column(String(6500))
    ru = Column(String(6500))

    def __repr__(self):
        return f"Sentence(id={self.id!r}, en={self.en!r}, ru={self.ru!r})"


class Ship(db.Model):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shame = Column(String(255))

    crew_id = Column(Integer, ForeignKey("crews.id"))
    crew = relationship("Crew", back_populates="ship", foreign_keys=[crew_id])

    details: Mapped[List["DetailCopy"]] = relationship(secondary="detail_copy_groups")

    def __repr__(self):
        return f"Ship(id={self.id!r}, shame={self.shame!r}, crew={self.crew!r})"


class Crew(db.Model):
    __tablename__ = "crews"

    id = Column(Integer, primary_key=True, autoincrement=True)

    token = Column(String(255), unique=True)
    name = Column(String(255), unique=True)

    ship = relationship("Ship", back_populates="crew")

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", foreign_keys=[owner_id])

    def __repr__(self):
        return f"Crew(name={self.name!r}, ship={self.ship!r}, token={self.token!r}, owner={self.owner!r})"


class DetailType(db.Model):
    __tablename__ = "detail_types"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name_id = Column(Integer, ForeignKey("sentences.id"))
    name = relationship("Sentence", foreign_keys=[name_id])

    description_id = Column(Integer, ForeignKey("sentences.id"))
    description = relationship("Sentence", foreign_keys=[description_id])

    def __repr__(self):
        return f"DetailType(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Detail(db.Model):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, autoincrement=True)

    kind_id = Column(Integer, ForeignKey("detail_types.id"))
    kind = relationship("DetailType", foreign_keys=[kind_id])

    cost = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)

    power_generation = Column(Integer)
    accel_factor = Column(Float)
    damage_absorption = Column(Integer)
    damage = Column(Integer)

    name_id = Column(Integer, ForeignKey("sentences.id"))
    name = relationship("Sentence", foreign_keys=[name_id])

    description_id = Column(Integer, ForeignKey("sentences.id"))
    description = relationship("Sentence", foreign_keys=[description_id])

    def __repr__(self):
        return f"Detail(id={self.id!r}, name={self.name!r}, description={self.description!r}, kind={self.kind!r}, cost={self.cost!r}, ...)"


class DetailCopy(db.Model):
    __tablename__ = "details_copies"

    id = Column(Integer, primary_key=True, autoincrement=True)

    ship_id = Column(Integer, ForeignKey("ships.id"))
    ship = relationship("Ship", foreign_keys=[ship_id])

    kind_id = Column(Integer, ForeignKey("details.id"))
    kind = relationship("Detail", foreign_keys=[kind_id])

    level = Column(Integer, default=1)

    def __repr__(self):
        return f"DetailCopy(id={self.id!r}, ship={self.ship!r}, kind={self.kind!r}, level={self.level!r})"


class RequiredShipDetail(db.Model):
    __tablename__ = "required_ship_details"

    id = Column(Integer, primary_key=True)
    detail_type_id = Column(Integer, ForeignKey("detail_types.id"))
    detail_type = relationship("DetailType", foreign_keys=[detail_type_id])

    def __repr__(self):
        return f"ReuqiredShipDetail(id={self.id!r}, detail_type={self.detail_type!r}"
