import random

from faker import Faker
from fastapi import APIRouter

from app.cerner.schemas import response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()
faker = Faker()


@router.get(
    "",
    summary="Get Patient List",
    response_description="The paginated list of patients",
    status_code=200,
    response_model=response.PaginatedPatientListResponse,
)
async def route_cerner_patient_list(
    _: CurrentUser, name: str | None = None, page: int = 1, size: int = 10
):
    """
    This endpoint returns a paginated list of patients
    """

    return {
        "data": [
            {
                "mrn": faker.ssn(),
                "name": f"{name} {faker.last_name()}" if name else faker.name(),
                "phone": random.choice([faker.phone_number(), None]),
                "email": random.choice([faker.email(), None]),
            }
            for _ in range(size + 1)
        ],
        "meta": {
            "total_no_items": 100,
            "total_no_pages": 10,
            "page": page,
            "size": size,
            "count": size,
            "has_next_page": page < 10,
            "has_prev_page": page > 1,
        },
    }
