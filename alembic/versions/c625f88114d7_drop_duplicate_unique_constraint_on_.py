"""drop duplicate unique constraint on cities city_name

Revision ID: c625f88114d7
Revises: 4ad8b62f4703
Create Date: 2026-08-31 14:57:50.688539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c625f88114d7'
down_revision: Union[str, Sequence[str], None] = '4ad8b62f4703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "cities_city_name_key", "cities", type_="unique"
    )


def downgrade() -> None:
    op.create_unique_constraint(
            "cities_city_name_key", "cities", ["city_name"]
        )
