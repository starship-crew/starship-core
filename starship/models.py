from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from starship import db


class Sentence(db.Model):
    __tablename__ = "sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    en: Mapped[str] = mapped_column(String(6500))
    ru: Mapped[str] = mapped_column(String(6500))

    def __repr__(self):
        return f"Sentence(id={self.id!r}, en={self.en!r}, ru={self.ru!r})"


class Ship(db.Model):
    __tablename__ = "ships"

    id: Mapped[int] = mapped_column(primary_key=True)
    shame: Mapped[int] = mapped_column(String(255))
    crew: Mapped["Crew"] = relationship(back_populates="ship")

    def __repr__(self):
        return f"Ship(id={self.id!r}, shame={self.shame!r}, crew={self.crew!r})"


class Crew(db.Model):
    __tablename__ = "crews"

    token: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    ship: Mapped["Ship"] = relationship(back_populates="crew")

    def __repr__(self):
        return f"Crew(name={self.name!r}, ship={self.ship!r}, token={self.token!r})"


class DetailType(db.Model):
    __tablename__ = "detail_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped["Sentence"] = relationship()
    description: Mapped["Sentence"] = relationship()

    def __repr__(self):
        return f"DetailType(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Detail(db.Model):
    __tablename__ = "detalis"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped["DetailType"] = relationship()

    cost: Mapped[int] = mapped_column(nullable=False)
    health: Mapped[int] = mapped_column(nullable=False)

    power_generation: Mapped[int] = mapped_column(Integer)
    accel_factor: Mapped[float] = mapped_column(Float)
    damage_absorption: Mapped[int] = mapped_column(Integer)
    damage: Mapped[int] = mapped_column(Integer)

    name: Mapped["Sentence"] = relationship()
    description: Mapped["Sentence"] = relationship()

    def __repr__(self):
        return f"Detail(id={self.id!r}, name={self.name!r}, description={self.description!r}, kind={self.kind!r}, cost={self.cost!r}, ...)"


class DetailCopy(db.Model):
    __tablename__ = "details_copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    ship: Mapped["Ship"] = relationship()
    kind: Mapped["Detail"] = relationship()
    level: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"DetailCopy(id={self.id!r}, ship={self.ship!r}, kind={self.kind!r}, level={self.level!r})"


class RequiredShipDetail(db.Model):
    __tablename__ = "required_ship_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    detail_type: Mapped["DetailType"] = relationship()

    def __repr__(self):
        return f"ReuqiredShipDetail(id={self.id!r}, detail_type={self.detail_type!r}"
