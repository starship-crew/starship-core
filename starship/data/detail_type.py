import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class DetailType(SqlAlchemyBase):
    __tablename__ = "detail_types"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    name_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    name = sa.orm.relationship("Sentence", foreign_keys=[name_id])

    description_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    description = sa.orm.relationship("Sentence", foreign_keys=[description_id])

    def __repr__(self):
        return f"DetailType(id={self.id!r}, name={self.name!r}, description={self.description!r})"
