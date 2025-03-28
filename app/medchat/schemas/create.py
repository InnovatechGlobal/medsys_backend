from typing import Literal

from pydantic import BaseModel


class MedChatMessageCreate(BaseModel):
    """
    Create schema for medchat messages
    """

    type: Literal["text"]
    content: str


class WsMedChatCreate(MedChatMessageCreate):
    """
    Create schema for ws med chat create
    """


class WsMedChatInteraction(MedChatMessageCreate):
    """
    Create schema for medchat interactions
    """

    chat_id: int
