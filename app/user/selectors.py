from sqlalchemy.ext.asyncio import AsyncSession

from app.user.crud import UserCRUD
from app.user.exceptions import UserDeactivated, UserNotFound


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
