from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, relationship

from app.core.database import DBBase


class Chat(DBBase):
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
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)

    messages: Mapped[list["ChatMessage"] | None] = relationship(
        "ChatMessage", lazy="immediate", backref="chats"
    )


class ChatMessage(DBBase):
    """
    Database model for chats
    """

    __tablename__ = "medchat_messages"

    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender = Column(Enum("system", "user", name="enum_chatmsg_sender"), nullable=False)
    type = Column(Enum("text", "audio", name="enum_chatmsg_type"), nullable=False)
    content = Column(Text, nullable=True)
    audio_url = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    attachment_name = Column(String, nullable=True)
    attachment_type = Column(
        Enum("img", "pdf", name="enum_attachment_type"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
