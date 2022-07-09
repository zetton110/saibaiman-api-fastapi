"""create_pump_settings_table

Revision ID: 6b6251db9366
Revises: d3112802d290
Create Date: 2022-07-07 15:51:39.942870

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = '6b6251db9366'
down_revision = 'd3112802d290'
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )
    
def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_pump_settings_table() -> None:
    op.create_table(
        "pump_settings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plant_id", sa.Integer, sa.ForeignKey("plants.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("need_pump", sa.Float, nullable=False),
        sa.Column("complete_pump", sa.Float, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_pump_settings_modtime
            BEFORE UPDATE
            ON pump_settings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_pump_settings_table()


def downgrade() -> None:
    op.drop_table("pump_settings")
    op.execute("DROP FUNCTION update_updated_at_column")