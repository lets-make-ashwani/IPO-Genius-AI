"""Create AI Analyses table

Revision ID: 004
Revises: 003
Create Date: 2026-07-17 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create ai_analyses table
    op.create_table(
        'ai_analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ipo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('business_analysis', sa.Text(), nullable=True),
        sa.Column('financial_analysis', sa.Text(), nullable=True),
        sa.Column('risk_analysis', sa.Text(), nullable=True),
        sa.Column('management_analysis', sa.Text(), nullable=True),
        sa.Column('valuation_analysis', sa.Text(), nullable=True),
        sa.Column('industry_analysis', sa.Text(), nullable=True),
        sa.Column('structured_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('financial_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('management_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('industry_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('risk_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('valuation_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('overall_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('confidence_reason', sa.Text(), nullable=True),
        sa.Column('recommendation', sa.String(length=50), nullable=False, server_default='Neutral'),
        sa.Column('source_hash', sa.String(length=64), nullable=True),
        sa.Column('provider', sa.String(length=100), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=True),
        sa.Column('prompt_version', sa.String(length=50), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('is_cached', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('cache_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ipo_id'], ['ipos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes on ai_analyses
    op.create_index(op.f('ix_ai_analyses_ipo_id'), 'ai_analyses', ['ipo_id'], unique=False)
    op.create_index(op.f('ix_ai_analyses_is_active'), 'ai_analyses', ['is_active'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_ai_analyses_is_active'), table_name='ai_analyses')
    op.drop_index(op.f('ix_ai_analyses_ipo_id'), table_name='ai_analyses')
    op.drop_table('ai_analyses')
