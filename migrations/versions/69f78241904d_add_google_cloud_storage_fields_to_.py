"""add google cloud storage fields to documents

Revision ID: 69f78241904d
Revises: 41197e1c49d6
Create Date: 2025-04-04 14:48:57.934806

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '69f78241904d'
down_revision: Union[str, None] = '41197e1c49d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Recreate all dropped tables."""
    # Create users table
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
                    sa.Column('first_name', sa.String(length=100), nullable=True),
                    sa.Column('last_name', sa.String(length=100), nullable=True),
                    sa.Column('username', sa.String(length=100), nullable=True),
                    sa.Column('phone_number', sa.String(length=20), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_telegram_id', 'users', ['telegram_id'], unique=True)

    # Create documents table with all fields including GCS fields
    op.create_table('documents',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('file_id', sa.String(length=255), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('mime_type', sa.String(length=100), nullable=True),
                    sa.Column('size', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('telegram_reminder_sent', sa.Boolean(), nullable=True),
                    sa.Column('sms_reminder_sent', sa.Boolean(), nullable=True),
                    sa.Column('call_reminder_sent', sa.Boolean(), nullable=True),
                    sa.Column('gcs_file_path', sa.String(length=255), nullable=True),
                    sa.Column('gcs_uploaded', sa.Boolean(), server_default=sa.text('false'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_documents_id', 'documents', ['id'], unique=False)
    op.create_index('ix_documents_file_id', 'documents', ['file_id'], unique=True)

    # Create statistics table
    op.create_table('statistics',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('message_count', sa.Integer(), nullable=True),
                    sa.Column('user_count', sa.Integer(), nullable=True),
                    sa.Column('document_count', sa.Integer(), nullable=True),
                    sa.Column('last_activity', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_statistics_id', 'statistics', ['id'], unique=False)


def downgrade() -> None:
    """Drop all recreated tables."""
    op.drop_index('ix_statistics_id', table_name='statistics')
    op.drop_table('statistics')
    op.drop_index('ix_documents_file_id', table_name='documents')
    op.drop_index('ix_documents_id', table_name='documents')
    op.drop_table('documents')
    op.drop_index('ix_users_telegram_id', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
