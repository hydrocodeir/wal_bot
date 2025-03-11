"""Add debt_days and status columns to admins

Revision ID: b179dc4ae62c
Revises: 
Create Date: 2025-03-03 19:30:01.300371

"""
from typing import Sequence, Union
from sqlalchemy.engine.reflection import Inspector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b179dc4ae62c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    columns = [col["name"] for col in inspector.get_columns("admins")]

    if "debt_days" not in columns:
        op.add_column("admins", sa.Column("debt_days", sa.Integer(), server_default="0"))

    if "status" not in columns:
        op.add_column("admins", sa.Column("status", sa.Boolean(), server_default="True"))

    columns = [col["name"] for col in inspector.get_columns("traffic_price")]

    if "dead_line" not in columns:
        op.add_column("traffic_price", sa.Column("dead_line", sa.Integer(), server_default="30"))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    columns = [col["name"] for col in inspector.get_columns("admins")]

    if "status" in columns:
        op.drop_column("admins", "status")

    if "debt_days" in columns:
        op.drop_column("admins", "debt_days")


    columns = [col["name"] for col in inspector.get_columns("traffic_price")]

    if "dead_line" in columns:
        op.drop_column("traffic_price", "dead_line")
