"""add medchat_messages.hiddden and metadata

Revision ID: 4e8921bfe08d
Revises: e6764a5f25c0
Create Date: 2025-04-06 12:30:48.665484

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e8921bfe08d"
down_revision: Union[str, None] = "e6764a5f25c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Globals
old_enum = "enum_attachment_type"
new_enum = "enum_attachment_type_new"


def upgrade() -> None:
    op.add_column(
        "medchat_messages",
        sa.Column("attachment_content", sa.Text, nullable=True),
    )
    op.add_column(
        "medchat_messages",
        sa.Column("hidden", sa.Boolean, server_default=sa.false(), nullable=False),
    )

    # Step 1: Create new enum type
    op.execute("CREATE TYPE {0} AS ENUM ('docx', 'pdf')".format(new_enum))

    # Step 2: Alter the column to use the new enum
    op.execute(f"""
        ALTER TABLE medchat_messages
        ALTER COLUMN attachment_type
        TYPE {new_enum}
        USING
            CASE
                WHEN attachment_type = 'img' THEN 'docx'::text::{new_enum}
                ELSE attachment_type::text::{new_enum}
            END
    """)

    # Step 3: Drop the old enum type
    op.execute("DROP TYPE {0}".format(old_enum))

    # Step 4: Rename new enum to original name
    op.execute("ALTER TYPE {0} RENAME TO {1}".format(new_enum, old_enum))


def downgrade() -> None:
    op.drop_column("medchat_messages", "attachment_content")
    op.drop_column("medchat_messages", "hidden")

    # Step 1: Recreate original enum
    op.execute("CREATE TYPE {0} AS ENUM ('img', 'pdf')".format(new_enum))

    # Step 2: Migrate column back
    op.execute(f"""
        ALTER TABLE medchat_messages
        ALTER COLUMN attachment_type
        TYPE {new_enum}
        USING
            CASE
                WHEN attachment_type = 'docx' THEN 'img'::text::{new_enum}
                ELSE attachment_type::text::{new_enum}
            END
    """)

    # Step 3: Drop current enum type
    op.execute("DROP TYPE {0}".format(old_enum))

    # Step 4: Rename back to original enum
    op.execute("ALTER TYPE {0} RENAME TO {1}".format(new_enum, old_enum))
