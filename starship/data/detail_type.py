import sqlalchemy as sa

from starship.helpers import get_lang

from .db_session import SqlAlchemyBase


class DetailType(SqlAlchemyBase):
    __tablename__ = "detail_types"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    string_id = sa.Column(sa.String, unique=True, nullable=False)
    order = sa.Column(sa.Integer, autoincrement=True)

    name_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    name = sa.orm.relationship(
        "Sentence",
        foreign_keys=[name_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )

    description_id = sa.Column(sa.Integer, sa.ForeignKey("sentences.id"))
    description = sa.orm.relationship(
        "Sentence",
        foreign_keys=[description_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )

    required = sa.Column(sa.Boolean, default=False)

    def __repr__(self):
        return f"DetailType(id={self.id!r}, string_id={self.string_id}, name={self.name!r}, description={self.description!r})"

    @property
    def as_response(self):
        lang = get_lang()
        return {
            "id": self.id,
            "string_id": self.string_id,
            "order": self.order,
            "name": self.name.get(lang),
            "description": self.description.get(lang),
            "required": self.required,
        }
