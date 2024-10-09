from pydantic import Field
from app.common.schemas import ResponseSchema
from app.user.schemas.base import User


class UserResponse(ResponseSchema):
    """
    Response schema for users
    """

    msg: str = "User retrieved successfully"
    data: User = Field(description="The user's details")
