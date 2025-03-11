from pydantic import Field

from app.cerner.schemas.base import (
    CernerAppointmentCalendarSummary,
    CernerAppointmentSummary,
    CernerHomepage,
)
from app.common.schemas import ResponseSchema


######################################################################
# Cerner Base
######################################################################
class CernerHomepageResponse(ResponseSchema):
    """
    Response schema for the cerner homepage
    """

    data: CernerHomepage = Field(description="The details of the cerner homepage")


######################################################################
# Cerner Appointment
######################################################################
class CernerAppointmentCalendarSummaryResponse(ResponseSchema):
    """
    Response schema for cerner appointment calendar summary
    """

    data: CernerAppointmentCalendarSummary = Field(
        description="The appointment calendar summary"
    )


class CernerAppointmentListResponse(ResponseSchema):
    """
    Response schema for cerner appointment list
    """

    data: list[CernerAppointmentSummary] = Field(description="The list of appointments")
