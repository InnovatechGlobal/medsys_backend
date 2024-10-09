from pydantic import BaseModel, EmailStr, Field


class HospitalCreate(BaseModel):
    """
    Create schema for hospitals
    """

    name: str = Field(max_length=150, description="The name of the hospital")
    address: str = Field(max_length=500, description="The address of the hospital")
    email: EmailStr = Field(max_length=255, description="The email of the hospital")
    phone: str = Field(max_length=20, description="The phone number of the hospital")
