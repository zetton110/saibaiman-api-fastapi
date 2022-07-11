"""create_notification_settings_table

Revision ID: 3e0e02fbff8c
Revises: 4bc4d170cd9f
Create Date: 2022-07-09 18:40:07.524817

"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = '3e0e02fbff8c'
down_revision = '4bc4d170cd9f'
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


def create_notification_settings_table() -> None:
    op.create_table(
        "notification_settings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("plant_id", sa.Integer, sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("service_type", sa.String, nullable=False),
        sa.Column("api_url", sa.String, nullable=False),
        sa.Column("access_token", sa.String, nullable=False),
        sa.Column("access_secret", sa.String, nullable=True),
        sa.Column("consumer_key", sa.String, nullable=True),
        sa.Column("consumer_secret", sa.String, nullable=True),
        sa.Column("enabled", sa.Boolean, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_notification_settings_modtime
            BEFORE UPDATE
            ON notification_settings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_notification_settings_table()


def downgrade() -> None:
    op.drop_table("notification_settings")
    op.execute("DROP FUNCTION update_updated_at_column")