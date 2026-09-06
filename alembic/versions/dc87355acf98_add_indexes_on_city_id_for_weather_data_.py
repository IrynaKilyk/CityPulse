"""add indexes on city_id for weather_data, air_quality, traffic_data

Revision ID: dc87355acf98
Revises: c625f88114d7
Create Date: 2026-09-06 17:44:12.315711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc87355acf98'
down_revision: Union[str, Sequence[str], None] = 'c625f88114d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_weather_data_city_id','weather_data', ['city_id'])
    op.create_index('ix_air_quality_city_id', 'air_quality', ['city_id'])
    op.create_index('ix_traffic_data_city_id', 'traffic_data', ['city_id'])

def downgrade() -> None:
    op.drop_index('ix_traffic_data_city_id', table_name='traffic_data')
    op.drop_index('ix_air_quality_city_id', table_name='air_quality')
    op.drop_index('ix_weather_data_city_id', table_name='weather_data')
