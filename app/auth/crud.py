from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import models
from app.common.crud import CRUDBase


class OAuth2LoginAttemptCRUD(CRUDBase[models.OAuth2UserLoginAttempt]):
    """
    CRUD Class for oauth2 login attempts
    """

    def __init__(self, db: AsyncSession):
        super().__init__(models.OAuth2UserLoginAttempt, db=db)


class RefreshTokenCRUD(CRUDBase[models.RefreshToken]):
    """
    CRUD Class for refresh tokens
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.RefreshToken, db=db)
