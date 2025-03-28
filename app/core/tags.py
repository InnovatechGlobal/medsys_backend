from functools import lru_cache

from pydantic import BaseModel


class RouteTags(BaseModel):
    """
    Base model for app route tags
    """

    # Auth
    AUTH: str = "Auth APIs"
    OAUTH2_ENDPOINT: str = "Oauth2 Endpoints"

    # User
    USER: str = "User APIs"

    # Medchat
    MEDCHAT: str = "MedChat APIs"

    # Hospital
    HOSPITAL: str = "Hospital APIs"

    # Integrations
    CERNER: str = "Cerner Endpoints"
    CERNER_APPOINTMENT: str = "Cerner Appointment APIs"
    CERNER_PATIENT: str = "Cerner Patient APIs"


@lru_cache
def get_tags():
    """
    Get app rotue tags
    """
    return RouteTags()
