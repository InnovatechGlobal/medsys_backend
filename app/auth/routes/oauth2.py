from datetime import date, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import AnyHttpUrl

from app.auth import services
from app.auth.annotations import BankIDOAuth2Services
from app.auth.crud import RefreshTokenCRUD
from app.auth.schemas import response
from app.auth.types import OAUTH2_SERVICES
from app.common.annotations import DatabaseSession
from app.common.exceptions import Unauthorized
from app.common.token import TokenGenerator
from app.common.utils import generate_state_token
from app.core.settings import get_settings
from app.external.criipto import utils as criipto_utils
from app.external.criipto.clients import InternalCriiptoVerifyClient
from app.user import formatters as user_formatters
from app.user import selectors as user_selectors
from app.user import services as user_services
from app.user.schemas import create as user_schemas_create

# Globals
router = APIRouter()
settings = get_settings()
criipto_verify_client = InternalCriiptoVerifyClient()
token_generator = TokenGenerator(secret_key=settings.SECRET_KEY)


@router.get(
    "/bankid",
    summary="Get list of bankid options",
    response_description="The list of available bankid options",
    status_code=status.HTTP_200_OK,
    response_model=response.BankIDOptionListResponse,
)
async def route_auth_oauth2_bankid_options():
    """
    This endpoint returns the list of available bankid login options
    """
    return {"data": [{"name": "Norwegian BankID", "code": "nobankid"}]}


@router.get(
    "/eid",
    summary="Get list of eid options",
    response_description="The list of available eid options",
    status_code=status.HTTP_200_OK,
    response_model=response.EIDOptionListResponse,
)
async def route_auth_oauth2_eid_options():
    """
    This endpoint returns the list of available e-id login options
    """
    return {"data": []}


@router.post(
    "",
    summary="Initialize SSO Login",
    response_description="Redirect to sso login",
    status_code=status.HTTP_200_OK,
    response_model=response.SSOLoginRequestResponse,
)
async def route_auth_oauth2_login(
    service: BankIDOAuth2Services, redirect_url: AnyHttpUrl, db: DatabaseSession
):
    """
    This endpoint initiates SSO Login
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
    "/verify",
    summary="Verify SSO Login",
    response_description="The user's details and tokens",
    status_code=status.HTTP_200_OK,
    response_model=response.UserLoginResponse,
)
async def route_auth_oauth2_verify(code: str, state: str, db: DatabaseSession):
    """
    This endpoint verifies the SSO login
    """

    # Verify oauth2_token
    oauth2_login_attempt = await services.verify_oauth2_token(
        state=state, service=OAUTH2_SERVICES.CRIIPTO_VERIFY.value, db=db
    )

    # Generate refresh and access token
    verify_response = await criipto_verify_client.verify_code(
        code=code, redirect_url=oauth2_login_attempt.redirect_url
    )

    # Get ID Token
    token = verify_response.get("id_token")
    if not token:
        raise Unauthorized("Invalid Login Request")

    # Decode token
    data = await criipto_utils.decode_token(token=verify_response["id_token"])

    # Get user
    user = await user_selectors.get_user(sub=data["sub"], db=db, raise_exc=False)

    # Check: user exists
    response_status = 200

    # Check: existing user but no account type
    if user and not bool(user.account_type):
        print(f"Forcefully set user[{user.id}] to INDIVIDUAL")
        user.account_type = "INDIVIDUAL"  # type: ignore
        await db.commit()

    if not user:
        user = await user_services.create_user(
            data=user_schemas_create.UserCreate(
                **{
                    "criipto_sub": data["sub"],
                    "full_name": data["name"],
                    "dob": date.fromisoformat(data["birthdate"]),
                    "country": data["country"],
                }
            ),
            db=db,
        )
        response_status = 201

    # Generate tokens
    access, refresh = await services.generate_user_tokens(user=user, db=db)

    return ORJSONResponse(
        content={
            "data": {
                "user": jsonable_encoder(await user_formatters.format_user(user=user)),
                "tokens": {"access_token": access, "refresh_token": refresh},
            }
        },
        status_code=response_status,
    )


@router.post(
    "/token",
    summary="Refresh Token",
    response_description="The new access token",
    status_code=status.HTTP_200_OK,
    response_model=response.TokenRefreshResponse,
)
async def route_oauth2_token(
    token: Annotated[str, Body(embed=True)], db: DatabaseSession
):
    """
    This endpoint refreshes the user's token
    """

    # Init crud
    token_crud = RefreshTokenCRUD(db=db)

    # Get refresh token
    token = await token_crud.get(content=token)
    if not token:
        raise Unauthorized("Invalid Refresh Token", loc=["body", "token"])

    # Check: expired
    if bool(datetime.now(timezone.utc) > token.expires_at.replace(tzinfo=timezone.utc)):
        raise Unauthorized("Refresh Token Has Expired", loc=["body", "token"])

    # Generate access token
    access_token = await token_generator.generate(
        sub=str(token.sub), refresh_token_id=token.id
    )

    return {"data": access_token}
