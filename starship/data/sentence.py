import yaml
import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class Sentence(SqlAlchemyBase):
    __tablename__ = "sentences"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    en = sa.Column(sa.String(6500), default="")
    ru = sa.Column(sa.String(6500), default="")

    def __repr__(self):
        return f"Sentence(id={self.id!r}, en={self.en!r}, ru={self.ru!r})"

    def to_yaml_string(self):
        obj = {"en": self.en, "ru": self.ru}
        return yaml.dump(obj, allow_unicode=True)
