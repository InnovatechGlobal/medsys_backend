from typing import Literal

from pydantic import BaseModel


class MedChatMessageCreate(BaseModel):
    """
    Create schema for medchat messages
    """

    type: Literal["text"]
    content: str | None


class WsMedChatCreate(MedChatMessageCreate):
    """
    Create schema for ws med chat create
    """


class WsMedChatInteraction(BaseModel):
    """
    Create schema for medchat interactions
    """

    chat_id: int
    msg: str
