"""Create IPO and IPODetail tables

Revision ID: 003
Revises: 002
Create Date: 2026-07-17 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create ipos table
    op.create_table(
        'ipos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('logo_url', sa.String(length=255), nullable=True),
        sa.Column('sector', sa.String(length=255), nullable=True),
        sa.Column('industry', sa.String(length=255), nullable=True),
        sa.Column('exchange', sa.String(length=50), nullable=False, server_default='BSE & NSE'),
        sa.Column('ipo_type', sa.String(length=50), nullable=False, server_default='MAINBOARD'),
        sa.Column('price_band', sa.String(length=100), nullable=False),
        sa.Column('lot_size', sa.Integer(), nullable=False),
        sa.Column('issue_size', sa.String(length=100), nullable=False),
        sa.Column('open_date', sa.Date(), nullable=False),
        sa.Column('close_date', sa.Date(), nullable=False),
        sa.Column('listing_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('gmp', sa.Integer(), nullable=True),
        sa.Column('gmp_last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('drhp_url', sa.String(length=500), nullable=True),
        sa.Column('rhp_url', sa.String(length=500), nullable=True),
        sa.Column('prospectus_url', sa.String(length=500), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_name'),
        sa.UniqueConstraint('slug')
    )

    # Create indexes on ipos table
    op.create_index(op.f('ix_ipos_company_name'), 'ipos', ['company_name'], unique=True)
    op.create_index(op.f('ix_ipos_slug'), 'ipos', ['slug'], unique=True)
    op.create_index(op.f('ix_ipos_status'), 'ipos', ['status'], unique=False)
    op.create_index(op.f('ix_ipos_open_date'), 'ipos', ['open_date'], unique=False)
    op.create_index(op.f('ix_ipos_listing_date'), 'ipos', ['listing_date'], unique=False)

    # Create ipo_details table
    op.create_table(
        'ipo_details',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ipo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_overview', sa.Text(), nullable=True),
        sa.Column('business_model', sa.Text(), nullable=True),
        sa.Column('promoters', sa.Text(), nullable=True),
        sa.Column('objectives', sa.Text(), nullable=True),
        sa.Column('financial_summary', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['ipo_id'], ['ipos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ipo_id')
    )

def downgrade() -> None:
    op.drop_table('ipo_details')
    op.drop_index(op.f('ix_ipos_listing_date'), table_name='ipos')
    op.drop_index(op.f('ix_ipos_open_date'), table_name='ipos')
    op.drop_index(op.f('ix_ipos_status'), table_name='ipos')
    op.drop_index(op.f('ix_ipos_slug'), table_name='ipos')
    op.drop_index(op.f('ix_ipos_company_name'), table_name='ipos')
    op.drop_table('ipos')
