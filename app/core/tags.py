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

    # Hospital
    HOSPITAL: str = "Hospital APIs"

    # Integrations
    CERNER: str = "Oracle Cerner APIs"


@lru_cache
def get_tags():
    """
    Get app rotue tags
    """
    return RouteTags()
