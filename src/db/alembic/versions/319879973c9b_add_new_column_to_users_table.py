"""Add new_column to users table

Revision ID: 319879973c9b
Revises: b179dc4ae62c
Create Date: 2025-03-14 12:46:36.438144

"""
from typing import Sequence, Union
from sqlalchemy.engine.reflection import Inspector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '319879973c9b'
down_revision: Union[str, None] = 'b179dc4ae62c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    columns = [col["name"] for col in inspector.get_columns("admins")]

    if "panel_id" not in columns:
        op.add_column("admins", sa.Column("panel_id", sa.Integer(), server_default="0"))

    columns = [col["name"] for col in inspector.get_columns("panels")]

    if "username" not in columns:
        op.add_column("panels", sa.Column("username", sa.String(), server_default=""))

    if "password" not in columns:
        op.add_column("panels", sa.Column("password", sa.String(), server_default=""))


def downgrade() -> None:    
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    columns = [col["name"] for col in inspector.get_columns("admins")]

    if "panel_id" in columns:
        op.drop_column("admins", "panel_id")

    columns = [col["name"] for col in inspector.get_columns("panels")]

    if "username" in columns:
        op.drop_column("panels", "username")
        
