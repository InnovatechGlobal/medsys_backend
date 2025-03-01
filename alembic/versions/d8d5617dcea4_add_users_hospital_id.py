"""add users.hospital_id

Revision ID: d8d5617dcea4
Revises: 03f740d85286
Create Date: 2025-03-01 21:13:19.853717

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8d5617dcea4"
down_revision: Union[str, None] = "03f740d85286"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "hospital_id",
            sa.Integer,
            sa.ForeignKey("hospitals.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "hospital_id")
