from datetime import datetime

from pydantic import BaseModel, Field


class MedChat(BaseModel):
    """
    Base schema for medchats
    """

    id: int = Field(description="The ID of the medchat")
    title: str = Field(description="The title of the chat")
    updated_at: datetime | None = Field(description="When the chat was last updated")
    created_at: datetime = Field(description="When the chat was created")
