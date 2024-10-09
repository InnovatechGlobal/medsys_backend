from typing import Any

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """
    Generic schema for token responses
    """

    access_token: str = Field(description="The access token")
    refresh_token: str = Field(description="The refresh token")


class ResponseSchema(BaseModel):
    """This is the generic base response schema"""

    status: str = Field(description="The response status", default="success")
    msg: str = Field(default="Request Successful", description="The response message")
    data: Any = Field(description="The response data")
