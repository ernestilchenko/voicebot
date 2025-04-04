"""recreate_dropped_tables

Revision ID: f75ebcd3596e
Revises: 69f78241904d
Create Date: 2025-04-04 15:00:15.474678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f75ebcd3596e'
down_revision: Union[str, None] = '69f78241904d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
