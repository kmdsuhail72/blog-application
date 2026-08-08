"""Add email verification to users

Revision ID: 4e1c2b8f9a6d
Revises: 3b99f2d11ae4
Create Date: 2026-08-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4e1c2b8f9a6d'
down_revision = '3b99f2d11ae4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column('users', 'is_verified', server_default=None)


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
