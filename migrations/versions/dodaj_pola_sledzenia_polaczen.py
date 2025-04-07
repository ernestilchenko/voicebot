"""dodaj_pola_śledzenia_połączeń

Revision ID: dodaj_pola_śledzenia_połączeń
Revises: f75ebcd3596e
Create Date: 2025-04-07 14:25:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dodaj_pola_śledzenia_połączeń'
down_revision: Union[str, None] = 'f75ebcd3596e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aktualizacja schematu."""
    # Dodanie nowych pól do śledzenia połączeń
    op.add_column('documents', sa.Column('call_attempts', sa.Integer(), server_default='0', nullable=False))
    op.add_column('documents', sa.Column('call_message_listened', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('documents', sa.Column('last_call_date', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Wycofanie zmian schematu."""
    op.drop_column('documents', 'last_call_date')
    op.drop_column('documents', 'call_message_listened')
    op.drop_column('documents', 'call_attempts')