from pydantic import BaseModel, Field


class BankIDOption(BaseModel):
    """
    Base schema for bank id options
    """

    name: str = Field(description="The service name")
    code: str = Field(description="The service code")


class EIDOption(BaseModel):
    """
    Base schema for e-id options
    """

    name: str = Field(description="The service name")
    code: str = Field(description="The service code")
