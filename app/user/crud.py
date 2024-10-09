from sqlalchemy.ext.asyncio import AsyncSession

from app.common.crud import CRUDBase
from app.user import models


class UserCRUD(CRUDBase[models.User]):
    """
    CRUD Class for user db interactions
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.User, db=db)
