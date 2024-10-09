from fastapi import APIRouter, status

from app.common.annotations import DatabaseSession
from app.hospital import services
from app.hospital.formatters import format_hospital
from app.hospital.schemas import create, response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()


@router.post(
    "",
    summary="Create Hospital/Organisation",
    response_description="The details of the hospital",
    status_code=status.HTTP_201_CREATED,
    response_model=response.HospitalResponse,
)
async def route_hospital_create(
    hospital_in: create.HospitalCreate, curr_user: CurrentUser, db: DatabaseSession
):
    """
    This endpoint creates a hospital/organization
    """

    # Create hospital
    hospital = await services.create_hospital(user=curr_user, data=hospital_in, db=db)

    return {"data": await format_hospital(hospital)}
