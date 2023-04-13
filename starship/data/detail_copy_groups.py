import sqlalchemy as sa

from .db_session import SqlAlchemyBase


detail_copy_groups = sa.Table(
    "detail_copy_groups",
    SqlAlchemyBase.metadata,
    sa.Column("detail_id", sa.ForeignKey("details_copies.id")),
    sa.Column("ship_id", sa.ForeignKey("ships.id")),
)
