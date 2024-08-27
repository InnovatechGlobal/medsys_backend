from datetime import datetime, timedelta

from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import selectors
from app.auth.crud import OAuth2LoginAttemptCRUD
from app.auth.schemas import create
from app.common.exceptions import Unauthorized
from app.core.settings import get_settings

# Globals
settings = get_settings()


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
