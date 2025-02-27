"""add new columns to admins and settings table

Revision ID: 8d1de7cb03de
Revises: 
Create Date: 2025-02-24 12:24:43.250096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d1de7cb03de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('admins', sa.Column('debt', sa.Integer(), server_default=sa.text("0")))
    op.add_column("settings", sa.Column("debt_system", sa.Boolean(), server_default=sa.text("0")))
    
    op.add_column('admins', sa.Column('traffic_new', sa.String()))
    op.execute('UPDATE admins SET traffic_new = traffic')
    op.drop_column('admins', 'traffic')
    op.alter_column('admins', 'traffic_new', new_column_name='traffic')

def downgrade() -> None:
    
    op.drop_column('admins', 'debt')
    op.drop_column("settings", "debt_system")

    op.add_column('admins', sa.Column('traffic_old', sa.Integer()))
    op.execute('UPDATE admins SET traffic_old = traffic')
    op.drop_column('admins', 'traffic')
    op.alter_column('admins', 'traffic_old', new_column_name='traffic')
