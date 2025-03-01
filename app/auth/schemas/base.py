from pydantic import BaseModel, Field

from app.common.schemas import TokenResponse
from app.user.schemas import base as user_base_schemas


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


class UserLogin(BaseModel):
    """
    Base schema for user login response
    """

    is_existing: bool = Field(
        description="This indicates if the user has an existing account or not"
    )
    user: user_base_schemas.User = Field(description="The user's details")
    tokens: TokenResponse = Field(description="The user's access and refresh tokens")
