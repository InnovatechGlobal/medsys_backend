from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """
    Create schema for users
    """

    full_name: str = Field(description="The user's full name")
    gender: Literal["MALE", "FEMALE", "OTHER"] | None = Field(
        default=None, description="The user's gender"
    )
    dob: date = Field(description="The user's dob")
    country: str = Field(description="The user's country", max_length=2)
    criipto_sub: str = Field(description="The user's criipto sub")
