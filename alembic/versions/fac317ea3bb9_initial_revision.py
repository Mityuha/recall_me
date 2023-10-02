"""initial revision

Revision ID: fac317ea3bb9
Revises:
Create Date: 2023-09-23 10:51:45.921648

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fac317ea3bb9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=128), nullable=False),
        sa.Column("event_day", sa.Integer(), nullable=False),
        sa.Column("event_month", sa.Integer(), nullable=False),
        sa.Column("voice_id", sa.String(length=128), nullable=True),
        sa.Column("source_text", sa.String(length=256), nullable=True),
        sa.Column("author_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "event_config",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Integer(), server_default="2", nullable=False),
        sa.Column("start_hour", sa.Integer(), server_default="-1", nullable=False),
        sa.Column(
            "notify_before_days", sa.Integer(), server_default="7", nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("event_config")
    op.drop_table("event")
    # ### end Alembic commands ###