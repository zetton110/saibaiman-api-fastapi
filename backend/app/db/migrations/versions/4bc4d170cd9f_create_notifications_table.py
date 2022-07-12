"""create_notifications_table

Revision ID: 4bc4d170cd9f
Revises: 6b6251db9366
Create Date: 2022-07-09 18:31:40.994562

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = '4bc4d170cd9f'
down_revision = '6b6251db9366'
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


def create_notifications_table() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plant_id", sa.Integer, sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("service_type", sa.String, nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("notified_to_service", sa.Boolean, nullable=False),
        sa.Column("snapshot_id", sa.Integer, sa.ForeignKey("snapshots.id"), nullable=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_notifications_modtime
            BEFORE UPDATE
            ON notifications
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_notifications_table()


def downgrade() -> None:
    op.drop_table("notifications")
    op.execute("DROP FUNCTION update_updated_at_column")