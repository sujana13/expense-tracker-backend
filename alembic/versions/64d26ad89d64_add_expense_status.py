"""add expense status

Revision ID: 64d26ad89d64
Revises: 2637f8fbaa59
Create Date: 2026-06-24 19:09:33.567753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64d26ad89d64"
down_revision = "2637f8fbaa59"
branch_labels = None
depends_on = None


def upgrade() -> None:

    expense_status = sa.Enum(
        "SUBMITTED",
        "APPROVED",
        "REJECTED",
        name="expensestatus"
    )

    expense_status.create(
        op.get_bind(),
        checkfirst=True
    )

    op.add_column(
        "expenses",
        sa.Column(
            "status",
            expense_status,
            nullable=False,
            server_default="SUBMITTED"
        )
    )


def downgrade() -> None:

    op.drop_column(
        "expenses",
        "status"
    )

    expense_status = sa.Enum(
        "SUBMITTED",
        "APPROVED",
        "REJECTED",
        name="expensestatus"
    )

    expense_status.drop(
        op.get_bind(),
        checkfirst=True
    )