from sqlalchemy.ext.asyncio import AsyncSession

from app.user.crud import UserCRUD
from app.user.schemas import create


async def create_user(data: create.UserCreate, db: AsyncSession):
    """
    Create a user obj

    Args:
        data (create.UserCreate): The user's details
        db (AsyncSession): The database session

    Returns:
        models.User: The created user obj
    """
    # Init crud
    user_crud = UserCRUD(db=db)

    # Create user
    user = await user_crud.create(data=data.model_dump())

    return user
