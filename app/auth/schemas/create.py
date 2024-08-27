from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.common.annotations import HttpUrlString


class OAuth2LoginAttemptCreate(BaseModel):
    """
    Create schema for oauth2login attempts
    """

    service: Literal["criipto_verify"] = Field(
        description="The service that initiated the login attempt"
    )
    redirect_url: HttpUrlString = Field(description="The redirect url")
    state_token: str = Field(description="The state token")
    created_at: datetime = Field(description="The time the token was created at")
    expires_at: datetime = Field(description="The time the token will expire")
