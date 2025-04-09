"""add: medchats patient deets

Revision ID: 35eeb24b5b90
Revises: 4e8921bfe08d
Create Date: 2025-04-09 09:55:23.992017

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "35eeb24b5b90"
down_revision: Union[str, None] = "4e8921bfe08d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "medchats",
        sa.Column("patient_id", sa.String, server_default="1", nullable=False),
    )
    op.add_column(
        "medchats",
        sa.Column(
            "patient_service", sa.String, server_default="cerner", nullable=False
        ),
    )
    op.add_column(
        "medchats",
        sa.Column(
            "patient_context", sa.Text, server_default="nocontext", nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_column("medchats", "patient_id")
    op.drop_column("medchats", "patient_service")
    op.drop_column("medchats", "patient_context")
