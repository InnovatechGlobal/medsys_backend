from typing import cast

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.crud import CRUDBase
from app.common.types import PaginationParamsType
from app.medchat import models
from app.user import models as user_models


class MedChatCRUD(CRUDBase[models.MedChat]):
    """
    CRUD Class for med chats
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.MedChat, db=db)

    async def get_list(
        self,
        user: user_models.User,
        pag: PaginationParamsType,
    ):
        """
        Get chat list
        """
        q = select(self.model).filter_by(
            user_id=user.id,
        )

        # Filter by q
        if pag.q:
            q = q.filter(self.model.title.ilike(f"%{pag.q}%"))

        # Order by
        if pag.order_by == "asc":
            q = q.order_by(self.model.created_at.asc())
        else:
            q = q.order_by(self.model.created_at.desc())

        # Paginate
        p_qs = q.limit(pag.size).offset(pag.size * (pag.page - 1))

        # Execute paginated qs
        results = await self.db.execute(p_qs)

        # Execute count query
        count = cast(
            int,
            # pylint: disable=not-callable
            await self.db.scalar(select(func.count()).select_from(q.subquery())),
        )

        return list(results.scalars().all()), count


class MedChatMessageCRUD(CRUDBase[models.MedChat]):
    """
    CRUD Class for med chat messages
    """

    def __init__(self, *, db: AsyncSession):
        super().__init__(models.MedChatMessage, db=db)
