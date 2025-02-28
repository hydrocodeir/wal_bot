"""add check columns

Revision ID: 2f32fbdf14a8
Revises: 
Create Date: 2025-02-28 15:50:23.664928

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = '2f32fbdf14a8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    inspector = inspect(op.get_bind())

    columns_admins = inspector.get_columns('admins')
    column_names_admins = [column['name'] for column in columns_admins]

    if 'debt' not in column_names_admins:
        op.add_column('admins', sa.Column('debt', sa.Integer(), server_default=sa.text("0")))

    if 'traffic_new' not in column_names_admins:
        op.add_column('admins', sa.Column('traffic_new', sa.String()))
        op.execute('UPDATE admins SET traffic_new = traffic')
        op.drop_column('admins', 'traffic')
        op.alter_column('admins', 'traffic_new', new_column_name='traffic')

    columns_settings = inspector.get_columns('settings')
    column_names_settings = [column['name'] for column in columns_settings]

    if 'debt_system' not in column_names_settings:
        op.add_column("settings", sa.Column("debt_system", sa.Boolean(), server_default=sa.text("0")))


def downgrade() -> None:
    inspector = inspect(op.get_bind())

    columns_admins = inspector.get_columns('admins')
    column_names_admins = [column['name'] for column in columns_admins]

    if 'debt' in column_names_admins:
        op.drop_column('admins', 'debt')

    columns_settings = inspector.get_columns('settings')
    column_names_settings = [column['name'] for column in columns_settings]

    if 'debt_system' in column_names_settings:
        op.drop_column("settings", "debt_system")

    if 'traffic' in column_names_admins:
        op.add_column('admins', sa.Column('traffic_old', sa.Integer()))
        op.execute('UPDATE admins SET traffic_old = traffic')
        op.drop_column('admins', 'traffic')
        op.alter_column('admins', 'traffic_old', new_column_name='traffic')