from pydantic import Field

from app.cerner.schemas.base import CernerHomepage
from app.common.schemas import ResponseSchema


class CernerHomepageResponse(ResponseSchema):
    """
    Response schema for the cerner homepage
    """

    data: CernerHomepage = Field(description="The details of the cerner homepage")
