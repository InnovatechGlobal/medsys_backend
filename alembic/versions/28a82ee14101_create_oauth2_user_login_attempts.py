"""
create: oauth2_user_login_attempts

Revision ID: 28a82ee14101
Revises:
Create Date: 2024-08-20 17:28:38.883855

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "28a82ee14101"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "oauth2_user_login_attempts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("service", sa.String(20), nullable=False),
        sa.Column("state_token", sa.String(10), unique=True, nullable=False),
        sa.Column("redirect_url", sa.String, nullable=False),
        sa.Column("is_used", sa.Boolean, server_default=sa.false(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("oauth2_user_login_attempts")
