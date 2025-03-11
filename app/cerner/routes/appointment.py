import random
from datetime import date as _date
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Query

from app.cerner.schemas import response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()


@router.get(
    "/calendar",
    summary="Get Appointment Calendar (Summary)",
    response_description="The appointment calendar summary",
    status_code=200,
    response_model=response.CernerAppointmentCalendarSummaryResponse,
)
async def route_cerner_appointment_calendar(
    year: Annotated[int, Query(gt=1900, le=2050)],
    month: Annotated[int, Query(ge=1, le=12)],
    _: CurrentUser,
):
    """
    This endpoint returns the cerner appointment calendar
    """

    # FILLER: Calculate the last day of the month
    if month == 12:
        next_month = _date(year + 1, 1, 1)
    else:
        next_month = _date(year, month + 1, 1)
    last_day_of_month = next_month - timedelta(days=1)

    return {
        "data": {
            "year": year,
            "month": month,
            "days": {
                current_date.isoformat(): {
                    "date": current_date.isoformat(),
                    "no_appointments": random.randint(
                        0, 10
                    ),  # Random count between 0 and 10
                }
                for current_date in (
                    _date(year, month, day)
                    for day in range(1, last_day_of_month.day + 1)
                )
            },
        }
    }


@router.get(
    "",
    summary="Get Appointments for a given day",
    response_description="The list of appointments",
    status_code=200,
    response_model=response.CernerAppointmentListResponse,
)
async def route_cerner_appointment_list(date: _date, _: CurrentUser):
    """
    This endpoint returns the list of appointments for the provided date
    """
    # Removes unused arg error
    del date
    
    return {
        "data": [
            {
                "id": "APID",
                "start_time": random.choice(["08:00", "09:00", "10:00"]),
                "end_time": random.choice(["10:00", "11:00", None]),
                "title": random.choice(["Emergency Follow-Up", "Imaging Consultation"]),
                "patient": "Alexis 2Pac",
                "doctor": "Dr. Babatunde William Vengeance",
            }
            for _ in range(0, 6)
        ]
    }
