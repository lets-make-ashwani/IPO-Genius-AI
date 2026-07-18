"""Create pipeline and document tables and add columns to ipos

Revision ID: 008
Revises: 007
Create Date: 2026-07-17 19:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '008'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Add columns to ipos table
    op.add_column('ipos', sa.Column('source_identifier', sa.String(length=255), nullable=True))
    op.add_column('ipos', sa.Column('source_data_hash', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_ipos_source_identifier'), 'ipos', ['source_identifier'], unique=False)

    # 2. Create pipeline_runs table
    op.create_table(
        'pipeline_runs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('idempotency_key', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('trigger', sa.String(length=50), nullable=False, server_default='MANUAL'),
        sa.Column('source_provider', sa.String(length=100), nullable=False),
        sa.Column('triggered_by_admin_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('total_discovered', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_processed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_skipped', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_failed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('run_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['triggered_by_admin_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pipeline_runs_idempotency_key'), 'pipeline_runs', ['idempotency_key'], unique=True)
    op.create_index(op.f('ix_pipeline_runs_status'), 'pipeline_runs', ['status'], unique=False)

    # 3. Create pipeline_run_items table
    op.create_table(
        'pipeline_run_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('run_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_identifier', sa.String(length=255), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('current_stage', sa.String(length=50), nullable=False, server_default='DISCOVERY'),
        sa.Column('ipo_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('source_data_hash', sa.String(length=64), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('extracted_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('normalized_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('validation_errors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_provider', sa.String(length=100), nullable=True),
        sa.Column('ai_model', sa.String(length=100), nullable=True),
        sa.Column('ai_tokens_used', sa.Integer(), nullable=True),
        sa.Column('ai_processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('ai_estimated_cost', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ipo_id'], ['ipos.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['run_id'], ['pipeline_runs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pipeline_run_items_run_id'), 'pipeline_run_items', ['run_id'], unique=False)
    op.create_index(op.f('ix_pipeline_run_items_status'), 'pipeline_run_items', ['status'], unique=False)

    # 4. Create ipo_documents table
    op.create_table(
        'ipo_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ipo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_type', sa.String(length=50), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('document_version', sa.String(length=50), nullable=False),
        sa.Column('document_hash', sa.String(length=64), nullable=False),
        sa.Column('document_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ipo_id'], ['ipos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('ipo_documents')
    op.drop_index(op.f('ix_pipeline_run_items_status'), table_name='pipeline_run_items')
    op.drop_index(op.f('ix_pipeline_run_items_run_id'), table_name='pipeline_run_items')
    op.drop_table('pipeline_run_items')
    op.drop_index(op.f('ix_pipeline_runs_status'), table_name='pipeline_runs')
    op.drop_index(op.f('ix_pipeline_runs_idempotency_key'), table_name='pipeline_runs')
    op.drop_table('pipeline_runs')
    op.drop_index(op.f('ix_ipos_source_identifier'), table_name='ipos')
    op.drop_column('ipos', 'source_data_hash')
    op.drop_column('ipos', 'source_identifier')
