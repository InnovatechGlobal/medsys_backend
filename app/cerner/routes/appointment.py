import random
from datetime import date, timedelta
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
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
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
                    date(year, month, day)
                    for day in range(1, last_day_of_month.day + 1)
                )
            },
        }
    }
