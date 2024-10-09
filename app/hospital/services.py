from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequest, InternalServerError
from app.hospital.crud import HospitalCRUD, HospitalStaffCRUD
from app.hospital.schemas import create
from app.user import models


async def create_hospital(
    user: models.User, data: create.HospitalCreate, db: AsyncSession
):
    # Init crud
    hospital_crud = HospitalCRUD(db=db)
    staff_crud = HospitalStaffCRUD(db=db)

    # Check: User does not belong to an org
    if bool(user.account_type == "ORGANIZATION"):
        # Check: User belongs to an org
        if await staff_crud.get(user_id=user.id):
            raise BadRequest(msg="User is already a part of an organization")

        # Edge Case: User is on an org account but doesnt belong to an org
        raise InternalServerError(
            msg=f"User[{user.id}] is on an org account but doesnt belong to an org",
            loc="app.hospital.services.create_hospital",
        )

    # Create Hospital
    hospital = await hospital_crud.create(data=data.model_dump())

    # Create Hospital Staff obj NOTE: dont commit
    await staff_crud.create(
        data={"hospital_id": hospital.id, "user_id": user.id}, commit=False
    )

    # Change user account type
    setattr(user, "account_type", "ORGANIZATION")

    # Commit all-or-nothing
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        await db.delete(hospital)
        await db.commit()
        raise

    return hospital
