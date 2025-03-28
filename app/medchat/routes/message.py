from typing import cast

from fastapi import APIRouter

from app.common.annotations import DatabaseSession
from app.common.exceptions import Forbidden
from app.common.paginators import get_pagination_metadata
from app.medchat import models, selectors
from app.medchat.crud import MedChatMessageCRUD
from app.medchat.formatters import format_medchat_message
from app.medchat.schemas import response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()


@router.get(
    "",
    summary="Get medchat messages",
    response_description="The list of medchat messages",
    status_code=200,
    response_model=response.PaginatedMedChatMessageListResponse,
)
async def route_medchat_message_list(
    medchat_id: int,
    curr_user: CurrentUser,
    db: DatabaseSession,
    page: int = 1,
    size: int = 10,
):
    """
    This endpoint returns the list of messages in a medchat
    """

    # Get medchat
    medchat = cast(
        models.MedChat, await selectors.get_medchat_by_id(id=medchat_id, db=db)
    )

    # Check: ownership
    if medchat.user_id != curr_user.id:  # type: ignore
        raise Forbidden("You are not allowed to access this chat")

    # Init crud
    msg_crud = MedChatMessageCRUD(db=db)

    # Get messages
    msgs, tno_msgs = await msg_crud.get_list(medchat=medchat, page=page, size=size)

    return {
        # NOTE: reverse messages so it will be top-bottom
        "data": [await format_medchat_message(msg=msg) for msg in msgs][::-1],
        "meta": await get_pagination_metadata(
            tno_items=tno_msgs, count=len(msgs), page=page, size=size
        ),
    }
