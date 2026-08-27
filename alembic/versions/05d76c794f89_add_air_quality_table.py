"""add air_quality table

Revision ID: 05d76c794f89
Revises: d16eb3e87bb3
Create Date: 2026-08-27 14:52:16.719187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05d76c794f89'
down_revision: Union[str, Sequence[str], None] = 'd16eb3e87bb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'air_quality',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('city_id', sa.Integer(), sa.ForeignKey('cities.id'), nullable=False ),
        sa.Column('recorded_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('pm10', sa.Float(), nullable=False),
        sa.Column('pm2_5', sa.Float(), nullable=False),
        sa.Column('carbon_monoxide', sa.Float(), nullable=False)
        )
    


def downgrade() -> None:
    op.drop_table('air_quality')
