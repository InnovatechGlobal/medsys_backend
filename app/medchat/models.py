from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, relationship

from app.core.database import DBBase


class MedChat(DBBase):
    """
    Database model for chats
    """

    __tablename__ = "medchats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    patient_id = Column(String, nullable=False)
    patient_service = Column(String, default="cerner", nullable=False)
    patient_context = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)

    messages: Mapped[list["MedChatMessage"] | None] = relationship(
        "MedChatMessage", lazy="immediate", backref="chats"
    )


class MedChatMessage(DBBase):
    """
    Database model for chats
    """

    __tablename__ = "medchat_messages"

    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(
        Integer,
        ForeignKey("medchats.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender = Column(Enum("system", "user", name="enum_chatmsg_sender"), nullable=False)
    type = Column(Enum("text", "audio", name="enum_chatmsg_type"), nullable=False)
    content = Column(Text, nullable=True)
    audio_url = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    attachment_name = Column(String, nullable=True)
    attachment_type = Column(
        Enum("docx", "pdf", name="enum_attachment_type"), nullable=True
    )
    attachment_content = Column(Text, nullable=True)
    hidden = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
