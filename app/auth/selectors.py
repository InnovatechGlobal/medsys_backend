from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crud import OAuth2LoginAttemptCRUD
from app.auth.exceptions import OAuth2LoginAttemptNotFound


async def get_ouath2_login_attempt(
    state_token: str, db: AsyncSession, raise_exc: bool = True
):
    """
    Get OAuth2LoginAttempt Obj

    Args:
        state_token (str): The state token
        db (AsyncSession): The database session
        raise_exception (bool = True): raise 404 exception if obj is not found

    Raises:
        OAuth2LoginAttemptNotFound

    Returns:
        models.OAuth2LoginAttempt | None
    """
    # Init crud
    oauth2_attempt_crud = OAuth2LoginAttemptCRUD(db=db)

    # Get obj
    obj = await oauth2_attempt_crud.get(state_token=state_token)
    if not obj and raise_exc:
        raise OAuth2LoginAttemptNotFound()

    return obj
