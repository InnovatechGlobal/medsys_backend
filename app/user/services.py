from sqlalchemy.ext.asyncio import AsyncSession

from app.hospital import services as hospital_services
from app.hospital.schemas import create as hc_schemas
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


async def setup_user_account(
    user: models.User, data: edit.UserAccountSetup, db: AsyncSession
):
    """
    Setup user account

    Args:
        user (models.User): The user obj
        data (edit.UserAccountSetup): The payload for user account setup
        db (AsyncSession): The database session

    Returns:
        models.User: The user obj
    """
    # NOTE: payloads for each account type will never be 'None' at this level due to the model_validator logic

    # Individual account setup
    if data.account_type == "INDIVIDUAL":
        user = await setup_individual_account(
            user=user,
            data=data.individual_payload,  # type: ignore
            db=db,
        )

    # Practitioner account setup
    elif data.account_type == "PRACTITIONER":
        user = await setup_practitioner_account(
            user=user,
            data=data.practitioner_payload,  # type: ignore
            db=db,
        )

    # Org account setup
    else:
        user, _ = await setup_organization_account(
            user=user,
            data=data.organization_payload,  # type: ignore
            db=db,
        )

    return user


async def setup_individual_account(
    user: models.User, data: edit.InvidiualUserAccountSetup, db: AsyncSession
):
    """
    Setup Individual user account

    Args:
        user (models.User): The user obj
        data (edit.InvidiualUserAccountSetup): The individual user account payload
        db (AsyncSession): The database session

    Returns:
        models.User: The user obj with individual account type
    """

    # Set values
    for field, value in data.model_dump().items():
        setattr(user, field, value)

    # Set account type
    setattr(user, "account_type", "INDIVIDUAL")

    # Save changes
    await db.commit()

    return user


async def setup_practitioner_account(
    user: models.User, data: edit.PractitionerUserAccountSetup, db: AsyncSession
):
    """
    Setup practitioner user account

    Args:
        user (models.User): The user obj
        data (edit.PractitionerUserAccountSetup): The practitioner user account payload
        db (AsyncSession): The database session

    Returns:
        models.User: The user obj with individual account type
    """

    # Set values
    for field, value in data.model_dump().items():
        setattr(user, field, value)

    # Set account type
    setattr(user, "account_type", "PRACTITIONER")

    # Save changes
    await db.commit()

    return user


async def setup_organization_account(
    user: models.User, data: hc_schemas.HospitalCreate, db: AsyncSession
):
    """
    Setup organization user account

    Args:
        user (models.User): The user obj
        data (hc_schemas.HospitalCreate): The organization/hospital create payload
        db (AsyncSession): The database session

    Returns:
        models.User, hospital_models.Hospital: The user obj with with hospital obj
    """
    # Create hospital
    hospital = await hospital_services.create_hospital(user=user, data=data, db=db)

    # Set account type
    setattr(user, "account_type", "ORGANIZATION")

    # Set hospital_id
    setattr(user, "hospital_id", hospital.id)

    # Save changes
    await db.commit()

    return user, hospital
