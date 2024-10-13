from datetime import date
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Base schema for users
    """

    id: UUID = Field(description="The user's ID")
    full_name: str = Field(description="The user's full name")
    email: str | None = Field(description="The user's email")
    gender: Literal["MALE", "FEMALE", "OTHER"] | None = Field(
        default=None, description="The user's gender"
    )
    medical_id: str | None = Field(description="The user's medical id")
    dob: date = Field(description="The user's dob")
    country: str = Field(description="The user's country", max_length=2)
    account_type: Literal["INDIVIDUAL", "PRACTITIONER", "ORGANIZATION"] | None = Field(
        description="The user's account type"
    )
    is_active: bool = Field(description="Indicates if the user's account is active")
