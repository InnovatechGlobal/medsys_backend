"""create: users

Revision ID: 95cdd49292f2
Revises: 28a82ee14101
Create Date: 2024-10-09 12:08:55.651663

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "95cdd49292f2"
down_revision: Union[str, None] = "28a82ee14101"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", PG_UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column(
            "gender",
            sa.Enum("MALE", "FEMALE", "OTHER", name="enum_genders"),
            nullable=False,
        ),
        sa.Column("medical_id", sa.String(12), nullable=True),
        sa.Column("dob", sa.Date, nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column(
            "account_type",
            sa.Enum(
                "INDIVIDUAL", "PRACTITIONER", "ORGANIZATION", name="enum_account_types"
            ),
            nullable=False,
        ),
        sa.Column("criipto_sub", sa.String(50), unique=True, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
