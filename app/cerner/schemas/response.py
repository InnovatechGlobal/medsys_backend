from pydantic import Field

from app.cerner.schemas.base import (
    CernerAppointmentCalendarSummary,
    CernerAppointmentSummary,
    CernerHomepage,
    PatientDetails,
    PatientSummary,
    PatientVitalSigns,
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


class PatientDetailsResponse(ResponseSchema):
    """
    Response schema for patient details
    """

    data: PatientDetails = Field(description="The details of the patient")


class PatientVitalSignsResponse(ResponseSchema):
    """
    Response schema for patient vital signs
    """

    data: PatientVitalSigns = Field(description="The patient's vital signs")
