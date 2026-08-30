"""create_traffic_table

Revision ID: 4ad8b62f4703
Revises: eb6f36cc21f9
Create Date: 2026-08-30 17:10:35.988041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ad8b62f4703'
down_revision: Union[str, Sequence[str], None] = 'eb6f36cc21f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'traffic_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('city_id', sa.Integer(), sa.ForeignKey('cities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('recorded_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('current_speed', sa.Integer(), nullable=False),
        sa.Column('free_flow_speed', sa.Integer(), nullable=False),
        sa.Column('current_travel_time', sa.Integer(), nullable=False),
        sa.Column('free_flow_travel_time', sa.Integer(), nullable=False),
        sa.Column('road_closure', sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('traffic_data')