from typing import Annotated

from fastapi import Depends
from pydantic import AfterValidator, AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import get_session, pagination_params
from app.common.types import PaginationParamsType

DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
PaginationParams = Annotated[PaginationParamsType, Depends(pagination_params)]
HttpUrlString = Annotated[AnyHttpUrl, AfterValidator(lambda v: str(v))]  # pylint: disable=unnecessary-lambda
