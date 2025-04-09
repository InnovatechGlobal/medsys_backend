from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class MedChat(BaseModel):
    """
    Base schema for medchats
    """

    id: int = Field(description="The ID of the medchat")
    title: str = Field(description="The title of the chat")
    updated_at: datetime | None = Field(description="When the chat was last updated")
    created_at: datetime = Field(description="When the chat was created")


######################################################################
# MedChat Message
######################################################################
class MedChatMessageAttachment(BaseModel):
    """
    Base schema for medchat message attachments
    """

    attachment_url: str | None = Field(description="The URL of the attachment")
    attachment_name: str | None = Field(description="The name of the attachment")
    attachment_type: Literal["img", "pdf", None] = Field(
        description="The type of the attachment"
    )


class MedChatMessage(BaseModel):
    """
    Base schema for medchat messages
    """

    id: int = Field(description="The ID of the message")
    sender: Literal["system", "user"] = Field(description="The sender of the message")
    type: Literal["text", "audio"] = Field(description="The message's type")
    content: str | None = Field(description="The text content of the message")
    audio_url: str | None = Field(description="The url of the audio")
    attachment: MedChatMessageAttachment | None = Field(
        description="The details of the medchat attachment"
    )
    created_at: datetime = Field(description="When the message was created")
