"""add unique constraint to cities city_name

Revision ID: d16eb3e87bb3
Revises: 
Create Date: 2026-08-24 12:44:02.499646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd16eb3e87bb3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_cities_city_name", "cities", ["city_name"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_cities_city_name", "cities", type_="unique"
    )
