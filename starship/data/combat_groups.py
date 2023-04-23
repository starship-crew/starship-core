import sqlalchemy as sa

from .db_session import SqlAlchemyBase

# combat_groups = sa.Table(
#     "combat_groups",
#     SqlAlchemyBase.metadata,
#     sa.Column("combat_id", sa.ForeignKey("combats.id", ondelete="CASCADE")),
#     sa.Column("crew_id", sa.ForeignKey("crews.id", ondelete="CASCADE")),
# )
