"""create cities and weather_data tables

Revision ID: 0ecab3a4c895
Revises: 
Create Date: 2026-08-31 14:32:25.538996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ecab3a4c895'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('city_name', sa.VARCHAR(), unique=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False)
    )

    op.create_table(
        'weather_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('city_id', sa.Integer(), sa.ForeignKey('cities.id'), nullable=False),
        sa.Column('recorded_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=False),
        sa.Column('relative_humidity', sa.Float(), nullable=False),
        sa.Column('wind_speed', sa.Float(), nullable=False),
        sa.Column('weather_code', sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('weather_data')
    op.drop_table('cities')
    
