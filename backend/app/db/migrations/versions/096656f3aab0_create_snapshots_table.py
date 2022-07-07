"""create_snapshots_table

Revision ID: 096656f3aab0
Revises: d8a625e7c659
Create Date: 2022-07-07 06:35:05.126153

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = '096656f3aab0'
down_revision = 'd8a625e7c659'
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

def create_snapshots_table() -> None:
    op.create_table(
        "snapshots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plant_id", sa.Integer, sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("image_file", sa.String, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_snapshots_modtime
            BEFORE UPDATE
            ON snapshots
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_snapshots_table()


def downgrade() -> None:
    op.drop_table("snapshots")
    op.execute("DROP FUNCTION update_updated_at_column")
