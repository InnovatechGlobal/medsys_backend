from typing import Literal

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.hospital.schemas import create as hc_schemas


class InvidiualUserAccountSetup(BaseModel):
    """
    Edit schema for invidiual user account setup
    """

    email: EmailStr = Field(description="The user's email")
    gender: Literal["MALE", "FEMALE", "OTHER"] = Field(description="The user's gender")


class PractitionerUserAccountSetup(BaseModel):
    """
    Edit schema for practitioner user account setup
    """

    email: EmailStr = Field(description="The user's email")
    gender: Literal["MALE", "FEMALE", "OTHER"] = Field(description="The user's gender")
    medical_id: str = Field(default=None, description="The user's medical id")


class UserAccountSetup(BaseModel):
    """
    Edit schema for user account setup
    """

    account_type: Literal["INDIVIDUAL", "PRACTITIONER", "ORGANIZATION"] = Field(
        description="The user's account type"
    )
    individual_payload: InvidiualUserAccountSetup | None = Field(
        default=None, description="The setup details for an individual user account"
    )
    practitioner_payload: PractitionerUserAccountSetup | None = Field(
        default=None, description="The setup details for a practitioner user account"
    )
    organization_payload: hc_schemas.HospitalCreate | None = Field(
        default=None, description="The details of the user's hospital"
    )

    @model_validator(mode="before")
    def val_valid_payload(cls, self: dict):  # type: ignore
        """
        Tasks:
            - Checks if the input provided matches the selected account type
        """

        # Check: individual account
        if self["account_type"] == "INDIVIDUAL":
            # Check: payload provided
            if not self["individual_payload"]:
                raise ValueError(
                    "You must provide the 'individual_payload' for INDIVIDUAL user accounts"
                )

            # Check: other payloads werent provided
            if self["practitioner_payload"] or self["organization_payload"]:
                raise ValueError(
                    "You must only provide the 'individual_payload' for INDIVIDUAL user accounts"
                )
        # Check: practitioner account
        elif self["account_type"] == "PRACTITIONER":
            # Check: payload provided
            if not self["practitioner_payload"]:
                raise ValueError(
                    "You must provide the 'practitioner_payload' for PRACTITIONER user accounts"
                )

            # Check: other payloads werent provided
            if self["individual_payload"] or self["organization_payload"]:
                raise ValueError(
                    "You must only provide the 'practitioner_payload' for PRACTITIONER user accounts"
                )

        # Check: organization account
        else:
            # Check: payload provided
            if not self["organization_payload"]:
                raise ValueError(
                    "You must provide the 'organization_payload' for ORGANIZATION user accounts"
                )

            # Check: other payloads werent provided
            if self["individual_payload"] or self["practitioner_payload"]:
                raise ValueError(
                    "You must only provide the 'organization_payload' for ORGANIZATION user accounts"
                )

        return self
