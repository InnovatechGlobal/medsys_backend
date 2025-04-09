import base64
from typing import Literal, Optional

from pydantic import BaseModel, field_validator


class MedChatMessageCreate(BaseModel):
    """
    Create schema for medchat messages
    """

    type: Literal["text"]
    content: str
    # NOTE: normal | comparisons raise an error
    attachment: Optional["MedChatAttachmentCreate"] = None


class MedChatAttachmentCreate(BaseModel):
    """
    Create schema for medchat attachments
    """

    file_type: Literal["pdf", "docx"]
    file_content: str

    @field_validator("file_content")
    def val_filecontent(cls, v: str):
        """
        Tasks:
            - Check if file content is valid base64
        """
        try:
            # Try to decode it
            base64.b64decode(v, validate=True)
        except Exception:
            raise ValueError("file_content must be a valid base64-encoded string")

        return v


class InternalMedChatAttachmentCreate(BaseModel):
    """
    Create schema for medchat attachments
    """

    attachment_url: str
    attachment_name: str
    attachment_type: Literal["pdf", "docx"]
    attachment_content: str


class WsMedChatCreate(MedChatMessageCreate):
    """
    Create schema for ws med chat create
    """

    patient_id: str


class WsMedChatInteraction(MedChatMessageCreate):
    """
    Create schema for medchat interactions
    """

    chat_id: int
