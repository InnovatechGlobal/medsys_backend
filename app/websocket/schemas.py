from typing import Literal

from pydantic import BaseModel


class BaseInputPayload(BaseModel):
    """
    Base ws input payload
    """

    type: Literal["medchat-create", "medchat-interaction"]
    data: dict
