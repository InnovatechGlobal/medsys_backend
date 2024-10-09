import secrets
from datetime import datetime, timedelta

from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import selectors
from app.auth.crud import OAuth2LoginAttemptCRUD, RefreshTokenCRUD
from app.auth.schemas import create
from app.common.exceptions import Unauthorized
from app.common.token import TokenGenerator
from app.core.settings import get_settings
from app.user import models as user_models

# Globals
settings = get_settings()
token_generator = TokenGenerator(secret_key=settings.SECRET_KEY)


async def create_oauth2_login_attempt(
    *,
    token: str,
    redirect_url: AnyHttpUrl,
    db: AsyncSession,
):
    """
    Create OAuth2 Login attempt

    Args:
        token (str): The state token
        redirect_url (AnyHttpUrl): The redirect url
        db (Session): The database session


    Returns:
        models.OAuth2LoginAttemptCRUD
    """
    # Init Crud
    oauth2_login_attempt_crud = OAuth2LoginAttemptCRUD(db=db)

    # Set timers
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=settings.OAUTH2_STATE_EXPIRE_MIN)

    # Create obj
    data = create.OAuth2LoginAttemptCreate(
        service="criipto_verify",
        redirect_url=redirect_url,
        state_token=token,
        created_at=created_at,
        expires_at=expires_at,
    )
    obj = await oauth2_login_attempt_crud.create(data=data.model_dump())

    return obj


async def verify_oauth2_token(state: str, service: str, db: AsyncSession):
    # Verify state token
    oauth2_login_attempt = await selectors.get_ouath2_login_attempt(
        state_token=state, db=db, raise_exc=False
    )

    # Check: token not found
    if not oauth2_login_attempt:
        raise Unauthorized("Invalid Token")

    # Check: correct service
    if oauth2_login_attempt.service != service:
        raise Unauthorized("Invalid Token")

    # Check: token is expired
    if (
        datetime.now(tz=oauth2_login_attempt.expires_at.tzinfo)
        > oauth2_login_attempt.expires_at
    ):
        raise Unauthorized("Expired Token")

    # Check: token is used
    if oauth2_login_attempt.is_used:
        raise Unauthorized("Token has been used")

    return oauth2_login_attempt


async def create_refresh_token(sub: str, db: AsyncSession):  # pylint: disable=redefined-builtin
    """
    Create refresh token obj.

    Args:
        sub (str): The refresh token sub.
        db (AsyncSession): The async db session.

    Returns:
        models.RefreshToken: The created refresh token.
    """
    # Init crud
    refresh_token_crud = RefreshTokenCRUD(db=db)

    # Create refresh token
    created_at = datetime.now()
    refresh_token = await refresh_token_crud.create(
        data={
            "sub": sub,
            "content": secrets.token_urlsafe(32),
            "expires_at": created_at
            + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS),
            "created_at": created_at,
        }
    )

    return refresh_token


async def generate_user_tokens(*, user: user_models.User, db: AsyncSession):
    """
    Generate user tokens

    Args:
        user (user_models.User): The user obj
        db (AsyncSession): The async db session

    Returns:
        Tuple (access_token, refresh_token): The user's access and refresh token
    """
    # Create refresh token
    ref_token = await create_refresh_token(sub=f"USER${user.id}", db=db)

    # Generate access token
    access_token = await token_generator.generate(
        sub=f"USER${user.id}", refresh_token_id=ref_token.id
    )

    # Update user last login
    user.last_login = ref_token.created_at
    await db.commit()

    return access_token, ref_token.content
