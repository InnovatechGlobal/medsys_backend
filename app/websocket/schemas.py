from typing import Literal

from pydantic import BaseModel


class BaseInputPayload(BaseModel):
    """
    Base ws input payload
    """

    type: Literal["medchat-create", "medchat-interaction"]
    data: dict


class MedChatAttachmentContentCheck(BaseModel):
    """
    Base schema for medchat attachment checks
    """

    is_valid: bool
