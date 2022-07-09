"""create_plants_table

Revision ID: d8a625e7c659
Revises: e956307552ac
Create Date: 2022-07-06 14:26:03.971250

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = 'd8a625e7c659'
down_revision = None
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

def create_plants_table() -> None:
    op.create_table(
        "plants",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("fullname", sa.String, nullable=True),
        sa.Column("plant_type", sa.String, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_plants_modtime
            BEFORE UPDATE
            ON plants
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_plants_table()


def downgrade() -> None:
    op.drop_table("plants")
    op.execute("DROP FUNCTION update_updated_at_column")
