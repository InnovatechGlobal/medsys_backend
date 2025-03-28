from pydantic import Field

from app.common.schemas import PaginatedResponseSchema
from app.medchat.schemas.base import MedChat


class PaginatedMedChatListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for medchats
    """

    data: list[MedChat] = Field(description="The list of medchats")
