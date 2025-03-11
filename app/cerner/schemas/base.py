from datetime import date as _date

from pydantic import BaseModel, Field


######################################################################
# Cerner Base
######################################################################
class PatientStatsChartEntry(BaseModel):
    """
    Base schema for the cerner patient stat entry
    """

    label: str = Field(description="The label of the data")
    tn_admitted: int = Field(description="The total number of admitted patients")
    tn_discharged: int = Field(description="The total number of discharged patients")


class CernerPatientStatsChart(BaseModel):
    """
    Base schema for the cerner patient statistics chart
    """

    weekly: list[PatientStatsChartEntry] = Field(
        description="The list of entires for the week"
    )
    monthly: list[PatientStatsChartEntry] = Field(
        description="The list of entires for the month"
    )
    yearly: list[PatientStatsChartEntry] = Field(
        description="The list of entires for the year"
    )


class CernerPatientDeptDist(BaseModel):
    """
    Base schema for the patient distribution by department
    """

    dept: str = Field(description="The name of the department")
    value: int = Field(description="The number of patients in the department")


class CernerMetricSummary(BaseModel):
    """
    Base schema for the cerner metric summary
    """

    name: str = Field(description="The name of the metric")
    obs: str = Field(description="The metric observation")


class CernerClinicMetricsSummary(BaseModel):
    """
    Base schema for the cerner clinical metrics summary
    """

    section: str = Field(description="The name of the section")
    metric: list[CernerMetricSummary] = Field(
        description="The list of metrics under the section"
    )


class CernerHomepage(BaseModel):
    """
    Base schema for the cerner homepage
    """

    tno_patients: int = Field(
        description="The total number of patients since last week"
    )
    tno_admissions: int = Field(
        description="The total number of recent admissions since last week"
    )
    tno_cases: int = Field(
        description="The total number of active cases since last week"
    )
    discharge_rate: float = Field(
        description="The discharge rate of patients in the past week"
    )
    patient_stats: CernerPatientStatsChart = Field(
        description="The patient statistics for week/month/year"
    )
    patient_dist: list[CernerPatientDeptDist] = Field(
        description="The patient distrubution by department"
    )
    clinic_metrics: list[CernerClinicMetricsSummary] = Field(
        description="The list of clinical metrics summaries"
    )


######################################################################
# Cerner Appointment
######################################################################
class CernerAppointmentCalendarSummaryDay(BaseModel):
    """
    Base schema representing a day/date on the cerner appointment calendar
    """

    date: _date = Field(description="The date of the calendar day")
    no_appointments: int = Field(description="The number of appointments on this day")


class CernerAppointmentCalendarSummary(BaseModel):
    """
    Base schema for cerner appointment calendar summary
    """

    year: int = Field(
        description="The year of the calendar",
    )
    month: int = Field(description="The month of the calendar")
    days: dict[_date, CernerAppointmentCalendarSummaryDay] = Field(
        default_factory=dict,
        description="A dictionary mapping dates to their appointment counts and details",
    )
