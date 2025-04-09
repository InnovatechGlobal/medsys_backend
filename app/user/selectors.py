from typing import Annotated, cast
from uuid import UUID

from fastapi import Header, HTTPException, Query, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.annotations import DatabaseSession
from app.common.exceptions import InvalidToken, Unauthorized
from app.common.token import TokenGenerator
from app.core.settings import get_settings
from app.user import models
from app.user.crud import UserCRUD
from app.user.exceptions import UserDeactivated, UserNotFound

# Globals
settings = get_settings()
token_generator = TokenGenerator(secret_key=settings.SECRET_KEY)


async def get_current_user(
    token: Annotated[str, Header(alias="Authorization")], db: DatabaseSession
):
    """
    Get the current logged in user
    """

    # Split token
    try:
        _, token = token.split(" ")
    except ValueError:
        raise InvalidToken(
            msg="Invalid Token Header, format is 'Bearer {token}",
            loc=["headers", "Authorization"],
        )

    # Get token sub / user ID
    sub: str = await token_generator.verify(token=token, sub_head="USER")

    return cast(models.User, await get_user_by_id(id=sub, db=db))


async def get_current_ws_user(
    ws: WebSocket, token: Annotated[str, Query()], db: DatabaseSession
):
    """
    Get the current logged in user
    """

    # Get token sub / user ID
    try:
        sub: str = await token_generator.verify(token=token, sub_head="USER")
    except HTTPException as e:
        raise Unauthorized(msg=e.detail)

    return cast(models.User, await get_user_by_id(id=sub, db=db))


async def get_user(
    sub: str, db: AsyncSession, raise_exc: bool = True, return_disabled: bool = False
):
    """
    Get user obj.

    Args:
        sub (str): The criipto sub of the user.
        db (AsyncSession): The async database session.
        raise_exc (bool = True): Raise a 404 if not found
        return_disabled (bool = False): return user even if user is not active

    Raises:
        UserNotFound

    Returns:
        models.User: The user obj.
    """
    # Init crud
    user_crud = UserCRUD(db=db)

    # Get obj
    obj = await user_crud.get(criipto_sub=sub)

    # Check: user exists
    if not obj and raise_exc:
        raise UserNotFound()

    # Check: user deactivated
    if obj and not bool(obj.is_active) and not return_disabled:
        raise UserDeactivated()

    return obj


async def get_user_by_id(
    id: str | UUID,  # pylint: disable=redefined-builtin
    db: AsyncSession,
    raise_exc: bool = True,
    return_disabled: bool = False,
):
    """
    Get user obj using the ID

    Args:
        id (str | UUID): The ID of the user
        db (AsyncSession): The async database session.
        raise_exc (bool = True): Raise a 404 if not found
        return_disabled (bool = False): return user even if user is not active

    Raises:
        UserNotFound

    Returns:
        models.User: The user obj.
    """
    # Init crud
    user_crud = UserCRUD(db=db)

    # Get obj
    obj = await user_crud.get(id=id)

    # Check: user exists
    if not obj and raise_exc:
        raise UserNotFound()

    # Check: user deactivated
    if obj and not bool(obj.is_active) and not return_disabled:
        raise UserDeactivated()

    return obj
