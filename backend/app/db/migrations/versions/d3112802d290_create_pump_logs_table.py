"""create_pump_logs_table

Revision ID: d3112802d290
Revises: a50be256e003
Create Date: 2022-07-07 15:30:18.844956

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = 'd3112802d290'
down_revision = 'a50be256e003'
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


def create_pump_logs_table() -> None:
    op.create_table(
        "pump_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plant_id", sa.Integer, sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_pump_logs_modtime
            BEFORE UPDATE
            ON pump_logs
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_pump_logs_table()


def downgrade() -> None:
    op.drop_table("pump_logs")
    op.execute("DROP FUNCTION update_updated_at_column")