import sqlalchemy as sa

from .db_session import SqlAlchemyBase


crew_groups = sa.Table(
    "crew_groups",
    SqlAlchemyBase.metadata,
    sa.Column("crew_id", sa.ForeignKey("crews.id")),
    sa.Column("user_id", sa.ForeignKey("users.id")),
)
