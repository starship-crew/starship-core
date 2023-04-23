import sqlalchemy as sa

from enum import Enum, auto

from .db_session import SqlAlchemyBase


class ActionKind(Enum):
    Attack = auto()
    Dodge = auto()
    FoolGiveUp = auto()
    SmartGiveUp = auto()
    SelfDestruct = auto()

    @property
    def as_response(self):
        return self.name


class Action(SqlAlchemyBase):
    __tablename__ = "actions"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    kind = sa.Column(sa.Enum(ActionKind))
    part_id = sa.Column(sa.Integer, sa.ForeignKey("details_copies.id"))
    part = sa.orm.relationship("DetailCopy")

    crew = sa.orm.relationship("Crew", back_populates="action")

    def __repr__(self):
        return (
            f"Action(id={self.id!r}, kind={self.kind.name!r}, part_id={self.part_id!r})"
        )

    @property
    def as_response(self):
        return {
            "kind": self.kind.as_response,
            "part": self.part.as_response if self.part else None,
        }
