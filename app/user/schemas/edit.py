from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserEdit(BaseModel):
    """
    Edit schema for users
    """

    email: EmailStr = Field(description="The user's email")
    gender: Literal["MALE", "FEMALE", "OTHER"] = Field(description="The user's gender")
    medical_id: str | None = Field(default=None, description="The user's medical id")
