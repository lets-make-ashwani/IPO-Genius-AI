"""User module settings and activities migration

Revision ID: 002
Revises: 001
Create Date: 2026-07-16 13:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Rename avatar -> avatar_url in users table
    op.alter_column('users', 'avatar', new_column_name='avatar_url')

    # Create settings table
    op.create_table(
        'settings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('theme', sa.String(length=50), nullable=False, server_default='light'),
        sa.Column('language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('timezone', sa.String(length=50), nullable=False, server_default='UTC'),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='USD'),
        sa.Column('email_notifications', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('push_notifications', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('marketing_emails', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('date_format', sa.String(length=50), nullable=False, server_default='YYYY-MM-DD'),
        sa.Column('time_format', sa.String(length=10), nullable=False, server_default='24h'),
        sa.Column('first_day_of_week', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    # Create user_activities table
    op.create_table(
        'user_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('user_activities')
    op.drop_table('settings')
    op.alter_column('users', 'avatar_url', new_column_name='avatar')
