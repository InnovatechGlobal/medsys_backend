from pydantic import BaseModel, Field


class Hospital(BaseModel):
    """
    Base schema for hospitals
    """

    id: int = Field(description="The ID of the hospital")
    name: str = Field(description="The name of the hospital")
    address: str = Field(description="The address of the hospital")
    email: str = Field(description="The email of the hospital")
    phone: str = Field(description="The phone number of the hospital")
