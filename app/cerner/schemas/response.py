from pydantic import Field

from app.cerner.schemas.base import (
    CernerAppointmentCalendarSummary,
    CernerAppointmentSummary,
    CernerHomepage,
    PatientSummary,
)
from app.common.schemas import PaginatedResponseSchema, ResponseSchema


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


######################################################################
# Patient
######################################################################
class PaginatedPatientListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for patient lists
    """

    data: list[PatientSummary] = Field(description="The list of patient summaries")
