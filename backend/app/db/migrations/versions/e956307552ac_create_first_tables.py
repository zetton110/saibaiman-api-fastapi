"""create_first_tables

Revision ID: e956307552ac
Revises: 
Create Date: 2022-07-06 08:44:42.456359

"""

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic
revision = 'e956307552ac'
down_revision = None
branch_labels = None
depends_on = None


def create_hedgehogs_table() -> None:
    op.create_table(
        "hedgehogs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("color_type", sa.Text, nullable=False),
        sa.Column("age", sa.Numeric(10, 1), nullable=False),
    )


def upgrade() -> None:
    create_hedgehogs_table()


def downgrade() -> None:
    op.drop_table("hedgehogs")