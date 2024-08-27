from fastapi import APIRouter, status
from pydantic import AnyHttpUrl

from app.auth import services
from app.auth.annotations import BankIDOAuth2Services
from app.auth.schemas import response
from app.auth.types import OAUTH2_SERVICES
from app.common.annotations import DatabaseSession
from app.common.utils import generate_state_token
from app.external.criipto.clients import InternalCriiptoVerifyClient

router = APIRouter()

# Clients
criipto_verify_client = InternalCriiptoVerifyClient()


@router.post(
    "/bankid",
    summary="SSO login with Norwegian Bank ID",
    response_description="Redirect to sso login",
    status_code=status.HTTP_200_OK,
    response_model=response.SSOLoginRequestResponse,
)
async def auth_oauth2_bankid_login(
    service: BankIDOAuth2Services, redirect_url: AnyHttpUrl, db: DatabaseSession
):
    """
    This endpoint initiates Norwegian bankID
    """

    # Generate state token
    token = await generate_state_token()

    # Create login attempt
    await services.create_oauth2_login_attempt(
        token=token, redirect_url=redirect_url, db=db
    )

    # Generate url
    url = await criipto_verify_client.generate_oauth2_url(
        service=service, token=token, redirect_url=redirect_url
    )
    return {
        "msg": "OAuth2 Redirect URL",
        "data": {"url": url},
    }


@router.post(
    "/nobankid/verify",
    summary="Verify Norwegian SSO Login",
    response_description="The user's details and tokens",
    status_code=status.HTTP_200_OK,
    # response_model=response.UserLoginResponse,
)
async def auth_oauth2_nobankid_verify(code: str, state: str, db: DatabaseSession):
    """
    This endpoint verifies the Norwegian bank ID SSO login
    """

    # Verify oauth2_token
    oauth2_login_attempt = await services.verify_oauth2_token(
        state=state, service=OAUTH2_SERVICES.CRIIPTO_VERIFY.value, db=db
    )

    # Generate refresh and access token
    _response = await criipto_verify_client.verify_code(
        code=code, redirect_url=oauth2_login_attempt.redirect_url
    )

    return _response
