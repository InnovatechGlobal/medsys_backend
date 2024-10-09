from pydantic import Field

from app.common.schemas import ResponseSchema
from app.hospital.schemas.base import Hospital


class HospitalResponse(ResponseSchema):
    """
    Response schema for hospitals
    """

    msg: str = "Hospital retrieved successfully"
    data: Hospital = Field(description="The details of the hospital")
