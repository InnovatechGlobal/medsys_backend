from pydantic import Field, HttpUrl

from app.auth.schemas.base import BankIDOption, EIDOption, UserLogin
from app.common.schemas import ResponseSchema


class BankIDOptionListResponse(ResponseSchema):
    """
    Response schema for available bank id login options
    """

    data: list[BankIDOption] = Field(description="The list of bankid options")


class EIDOptionListResponse(ResponseSchema):
    """
    Response schema for available e-id login options
    """

    data: list[EIDOption] = Field(description="The list of e-id options")


class SSOLoginRequestResponse(ResponseSchema):
    """
    Response schema for sso login response
    """

    data: dict[str, HttpUrl] = Field("The SSO Redirect URL")


class UserLoginResponse(ResponseSchema):
    """
    Response schema for user login
    """

    data: UserLogin = Field(description="The user's access and refresh tokens")


class TokenRefreshResponse(ResponseSchema):
    """
    Response schema for token refresh
    """

    msg: str = "Access token refreshed successfully"
    data: str = Field(description="The new access token")
