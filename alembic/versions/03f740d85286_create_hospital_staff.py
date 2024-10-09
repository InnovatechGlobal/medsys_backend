"""create: hospital_staff

Revision ID: 03f740d85286
Revises: 39ab41563ffa
Create Date: 2024-10-09 22:15:44.161210

"""

from enum import auto
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "03f740d85286"
down_revision: Union[str, None] = "39ab41563ffa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hospital_staff",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "hospital_id",
            sa.Integer,
            sa.ForeignKey("hospitals.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            PG_UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("hospital_staff")
