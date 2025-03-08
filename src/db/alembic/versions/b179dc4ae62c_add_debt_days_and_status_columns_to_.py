"""Add debt_days and status columns to admins

Revision ID: b179dc4ae62c
Revises: 
Create Date: 2025-03-03 19:30:01.300371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b179dc4ae62c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('admins', sa.Column('debt_days', sa.Integer(), server_default='0'))
    op.add_column('admins', sa.Column('status', sa.Boolean(), server_default=('True')))
    op.add_column('traffic_price', sa.Column('dead_line', sa.Integer(), server_default='30'))



def downgrade() -> None:
    op.drop_column('admins', 'status')
    op.drop_column('admins', 'debt_days')
    op.drop_column('traffic_price', 'dead_line')

