from pydantic import Field

from app.auth.schemas.base import BankIDOption, EIDOption
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

    data: dict[str, str]


class UserLoginResponse(ResponseSchema):
    """
    Response schema for user login
    """
