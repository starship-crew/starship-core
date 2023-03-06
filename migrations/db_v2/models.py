from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


user = "root"
password = "toor"  # plain (unescaped) text
host = "localhost"
db_name = "starship"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{db_name}", echo=False
)
Base = declarative_base()


class Crew(Base):
    __tablename__ = "crews"

    token = Column(String(255), primary_key=True)
    name = Column(String(255), unigue=True)
    ship = Column(Integer, ForeignKey("ships.id"))

    Ship = relationship("Ship")


class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True)
    shame = Column(String(255))


class DetailCopy(Base):
    __tablename__ = "details_copies"

    id = Column(Integer, primary_key=True)
    ship = Column(Integer, ForeignKey("ships.id"))
    kind = Column(Integer, ForeignKey("details.id"))

    ship = relationship("Ship")
    detail = relationship("Detail")


class Detail(Base):
    __tablename__ = "detalis"

    id = Column(Integer, primary_key=True)
    kind = Column(Integer, ForeignKey("details_types.id"))
    cost = Column(Integer, nullable=False)
    health = Column(Integer, nullale=False)
    power_generation = Column(Integer)
    accel_factor = Column(Float)
    damage_absorption = Column(Integer)
    damage = Column(Integer)
    name = Column(Integer, ForeignKey("senteces.id"))
    description = Column(Integer, ForeignKey("sentences.id"))

    details_types = relationship("DetailType")
    sentences = relationship("Sentence")


class DetailType(Base):
    __tablename__ = "detail_types"

    id = Column(Integer, primare_key=True)
    name = Column(Integer, ForeignKey("sentences.id"))
    description = Column(Integer, ForeignKey("sentences.id"))

    sentences = relationship("Sentence")


class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True)
    en = Column(String(6500))
    ru = Column(String(6500))


class RequiredShipDetail(Base):
    __tablename__ = "required_ship_details"

    detail_types = Column(Integer, ForeignKey("detail_types.id"))

    detal_types = relationship("DetailType")


Base.metadata.create_all(engine)