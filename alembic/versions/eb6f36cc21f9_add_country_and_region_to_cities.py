"""add country and region to cities

Revision ID: eb6f36cc21f9
Revises: 05d76c794f89
Create Date: 2026-08-29 15:48:24.534427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb6f36cc21f9'
down_revision: Union[str, Sequence[str], None] = '05d76c794f89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "cities",
        sa.Column("country", sa.String(length=100), nullable=True)
        )
    op.add_column(
        "cities",
        sa.Column("region", sa.String(length=100), nullable=True)
        )


def downgrade() -> None:
    op.drop_column("cities","country")
    op.drop_column("cities", "region")
