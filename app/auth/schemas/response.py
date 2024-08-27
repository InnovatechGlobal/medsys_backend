from app.common.schemas import ResponseSchema


class SSOLoginRequestResponse(ResponseSchema):
    """
    Response schema for sso login response
    """

    data: dict[str, str]


class UserLoginResponse(ResponseSchema):
    """
    Response schema for user login
    """
