from sqlalchemy.ext.asyncio import AsyncSession

from app.common.crud import CRUDBase
from app.medchat import models


class MedChatCRUD(CRUDBase[models.MedChat]):
    """
    CRUD Class for med chats
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.MedChat, db=db)


class MedChatMessageCRUD(CRUDBase[models.MedChat]):
    """
    CRUD Class for med chat messages
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.MedChatMessage, db=db)
