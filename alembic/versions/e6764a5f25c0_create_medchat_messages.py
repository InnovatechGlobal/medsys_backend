"""create: medchat_messages

Revision ID: e6764a5f25c0
Revises: c3ef07a6322f
Create Date: 2025-03-27 22:17:42.475792

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e6764a5f25c0"
down_revision: Union[str, None] = "c3ef07a6322f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "medchat_messages",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column(
            "chat_id",
            sa.Integer,
            sa.ForeignKey("chats.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "sender",
            sa.Enum("system", "user", name="enum_chatmsg_sender"),
            nullable=False,
        ),
        sa.Column(
            "type", sa.Enum("text", "audio", name="enum_chatmsg_type"), nullable=False
        ),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column("audio_url", sa.String, nullable=True),
        sa.Column("attachment_url", sa.String, nullable=True),
        sa.Column("attachment_name", sa.String, nullable=True),
        sa.Column(
            "attachment_type",
            sa.Enum("img", "pdf", name="enum_attachment_type"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("medchat_messages")
