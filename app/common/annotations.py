from typing import Annotated

from fastapi import Depends
from pydantic import AfterValidator, AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dependencies import get_session

DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
HttpUrlString = Annotated[AnyHttpUrl, AfterValidator(lambda v: str(v))]  # pylint: disable=unnecessary-lambda
