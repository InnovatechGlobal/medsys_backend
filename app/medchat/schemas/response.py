from pydantic import Field

from app.common.schemas import PaginatedResponseSchema
from app.medchat.schemas.base import MedChat, MedChatMessage


class PaginatedMedChatListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for medchats
    """

    data: list[MedChat] = Field(description="The list of medchats")


class PaginatedMedChatMessageListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for medchat messages
    """

    data: list[MedChatMessage] = Field(description="The list of medchat messages")
