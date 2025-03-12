from datetime import date as _date
from datetime import time as _time

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


class CernerAppointmentSummary(BaseModel):
    """
    Base schema for cerner appointment summary
    """

    id: str = Field(description="The ID of the appointment")
    start_time: _time = Field(description="The time of the appointment")
    end_time: _time | None = Field(
        default=None,
    )
    title: str = Field(description="The title of the appointment")
    patient: str = Field(description="The name of the patient")
    doctor: str = Field(description="The name of the doctor")


######################################################################
# Patient
######################################################################
class PatientSummary(BaseModel):
    """
    Base schema for patient summaries
    """

    id: str = Field(description="The patient's ID")
    mrn: str = Field(description="The patient's mrn")
    name: str = Field(description="The patient's name")
    phone: str | None = Field(description="The patient's phone number")
    email: str | None = Field(description="The patient's email address")


class PatientDetails(BaseModel):
    """
    Base schema for patient details
    """

    id: str = Field(description="The patient's ID")
    mrn: str = Field(description="The patient's mrn")
    name: str = Field(description="The patient's name")
    phone: str | None = Field(description="The patient's phone number")
    email: str | None = Field(description="The patient's email address")
    age: int = Field(description="The age of the patient")
    gender: str = Field(description="The patient's gender")
    address: str = Field(description="The patient's address")


class PatientVitalSigns(BaseModel):
    """
    Base schema for patient vital signs
    """

    bp: str | None = Field(description="The patient's blood pressure")
    heart_rate: int = Field(description="The patient's heart rate in bpm")
    temp: float | None = Field(description="The patient's recorded temp in degrees cel")
    height: float | None = Field(description="The patient's height in meters")
    weight: float | None = Field(description="The patient's weight in kg")
    bmi: float | None = Field(description="The patient's body mass index in kg/m3")


class PatitentLabAndSurgicalReport(BaseModel):
    """
    Base schema for patient lab and sergical reports
    """

    name: str = Field(description="The title of the report")
    url: str = Field(description="The URL of the report")
    uploaded_on: _date = Field(description="Indicator for when the report was uploaded")
