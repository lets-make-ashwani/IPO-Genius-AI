"""Create Watchlist tables

Revision ID: 005
Revises: 004
Create Date: 2026-07-17 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create watchlist_folders table
    op.create_table(
        'watchlist_folders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'name', name='uq_user_folder_name')
    )
    op.create_index(op.f('ix_watchlist_folders_user_id'), 'watchlist_folders', ['user_id'], unique=False)

    # 2. Create watchlist_items table
    op.create_table(
        'watchlist_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('folder_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ipo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='MEDIUM'),
        sa.Column('reminder_enabled', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reminder_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ai_overall_score', sa.Integer(), nullable=True),
        sa.Column('ai_recommendation', sa.String(length=50), nullable=True),
        sa.Column('ai_confidence_score', sa.Float(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['folder_id'], ['watchlist_folders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ipo_id'], ['ipos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watchlist_items_folder_id'), 'watchlist_items', ['folder_id'], unique=False)
    op.create_index(op.f('ix_watchlist_items_ipo_id'), 'watchlist_items', ['ipo_id'], unique=False)

    # 3. Create partial unique index for active folder + ipo
    op.create_index(
        'ix_active_folder_ipo',
        'watchlist_items',
        ['folder_id', 'ipo_id'],
        unique=True,
        postgresql_where=sa.text('deleted_at IS NULL')
    )

def downgrade() -> None:
    op.drop_index('ix_active_folder_ipo', table_name='watchlist_items')
    op.drop_index(op.f('ix_watchlist_items_ipo_id'), table_name='watchlist_items')
    op.drop_index(op.f('ix_watchlist_items_folder_id'), table_name='watchlist_items')
    op.drop_table('watchlist_items')

    op.drop_index(op.f('ix_watchlist_folders_user_id'), table_name='watchlist_folders')
    op.drop_table('watchlist_folders')
