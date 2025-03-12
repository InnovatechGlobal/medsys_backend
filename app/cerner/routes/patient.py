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
                "id": str(faker.random_number(5, fix_len=True)),
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


@router.get(
    "/{patient_id}/",
    summary="Get patient details",
    response_description="The patient's details",
    status_code=200,
    response_model=response.PatientDetailsResponse,
)
async def route_cerner_patient_details(patient_id: str, _: CurrentUser):
    """
    This enpoint returns the details of the patient
    """

    return {
        "data": {
            "id": patient_id,
            "mrn": faker.ssn(),
            "name": faker.name(),
            "phone": random.choice([faker.phone_number(), None]),
            "email": random.choice([faker.email(), None]),
            "age": random.randint(1, 90),
            "gender": random.choice(["Male", "Female"]),
            "address": faker.address(),
        }
    }


@router.get(
    "/{patient_id}/vitals",
    summary="Get Patient Vitals",
    response_description="The patient's vitals",
    status_code=200,
    response_model=response.PatientVitalSignsResponse,
)
async def route_cerner_patient_vitals(patient_id: str, _: CurrentUser):
    """
    This endpoint returns the patient's vital signs
    """

    # Remove unused args
    del patient_id

    return {
        "data": {
            "bp": random.choice(["135/85", None]),
            "heart_rate": random.choice([random.randint(60, 120), None]),
            "temp": random.choice([random.randint(36, 40), None]),
            "height": random.choice([1, 7, 1.8, 1.9, None]),
            "weight": random.choice([random.randint(50, 100), None]),
            "bmi": random.choice([random.randint(20, 30), None]),
        }
    }


@router.get(
    "/{patient_id}/med-history",
    summary="Get patient medical history (Not Functional)",
    response_description="The list of the patient's medical history",
    status_code=200,
    response_model=None,
    deprecated=True,
)
async def route_cerner_patient_medhistory_list():
    """
    This endpoint returns the list of the patient's medical history
    """


@router.get(
    "/{patient_id}/treatment-history",
    summary="Get patient treatment history (Not Functional)",
    response_description="The list of the patient's treatment history",
    status_code=200,
    response_model=None,
    deprecated=True,
)
async def route_cerner_patient_treatment_history_list():
    """
    This endpoint returns the list of the patient's treatment history
    """


@router.get(
    "/{patient_id}/reports",
    summary="Get patient lab reports (URLS are invalid)",
    response_description="The list of the patient's lab reports",
    status_code=200,
    response_model=response.PatientLabAndSurgicalReportListResponse,
)
async def route_cerner_patient_report_list(_: CurrentUser):
    """
    This endpoint returns the list of the patient's lab reports
    """

    return {
        "data": [
            {"name": f"Report {i}", "url": faker.url(), "uploaded_on": faker.date()}
            for i in range(random.randint(1, 10))
        ]
    }
