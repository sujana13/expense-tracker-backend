"""add paid to expense status

Revision ID: bd26024494fb
Revises: 3da8f77cfea6
Create Date: 2026-07-21 13:13:17.671719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd26024494fb'
down_revision: Union[str, Sequence[str], None] = '3da8f77cfea6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "ALTER TYPE expensestatus ADD VALUE IF NOT EXISTS 'PAID';"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
