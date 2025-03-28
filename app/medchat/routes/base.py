from fastapi import APIRouter

from app.common.annotations import DatabaseSession, PaginationParams
from app.common.paginators import get_pagination_metadata
from app.medchat.crud import MedChatCRUD
from app.medchat.formatters import format_medchat
from app.medchat.schemas import response
from app.user.annotations import CurrentUser

# Globals
router = APIRouter()


@router.get(
    "",
    summary="Get MedChats",
    response_description="The paginated list of medchats",
    status_code=200,
    response_model=response.PaginatedMedChatListResponse,
)
async def route_medchat_list(
    pag: PaginationParams, curr_user: CurrentUser, db: DatabaseSession
):
    """
    This endpoint is used to get the list of medchats
    """

    # init crud
    medchat_crud = MedChatCRUD(db=db)

    # Get medchats
    medchats, tno_medchats = await medchat_crud.get_list(user=curr_user, pag=pag)

    return {
        "data": [await format_medchat(medchat=medchat) for medchat in medchats],
        "meta": await get_pagination_metadata(
            tno_items=tno_medchats, count=len(medchats), page=pag.page, size=pag.size
        ),
    }
