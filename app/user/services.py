from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequest
from app.user import models
from app.user.crud import UserCRUD
from app.user.schemas import create, edit


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


async def set_user(
    user: models.User,
    account_type: Literal["INDIVIDUAL", "PRACTITIONER"],
    data: edit.UserEdit,
    db: AsyncSession,
):
    """
    Set user obj i.e. set initial details

    Args:
        user (models.User): The user obj
        account_type ("INDIVIDUAL", "PRACTITIONER"): The user's account type
        data (edit.UserEdit): The user's initial details
        db (AsyncSession): The database session

    Raises:
        BadRequest

    Returns:
        models.User: The updated user obj
    """
    # Init crud
    user_crud = UserCRUD(db=db)

    # Edit email
    if bool(user.email != data.email):
        # Check: email isnt taken
        if await user_crud.get(email=data.email):
            raise BadRequest(msg="User with email exist", loc=["body", "email"])

        # Update email
        setattr(user, "email", data.email)

    # Edit Gender
    if bool(user.gender != data.gender):
        setattr(user, "gender", data.gender)

    # Check: only practitioners can have medical_ids
    if data.medical_id and account_type != "PRACTITIONER":
        raise BadRequest(
            msg="Only practitioners can have a medical id", loc=["body", "medical_id"]
        )

    # Edit medical ID
    if bool(user.medical_id != data.medical_id):
        setattr(user, "medical_id", data.medical_id)

    # Set Account Type
    if not bool(user.account_type):
        # Check: practitioners must have medical IDs
        if account_type == "PRACTITIONER" and not data.medical_id:
            raise BadRequest(
                "Practitioners must have medical IDs", loc=["body", "medical_id"]
            )

        # Set account type
        setattr(user, "account_type", account_type)

    # Save changes
    await db.commit()

    return user
