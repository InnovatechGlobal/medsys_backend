from typing import Literal
from fastapi import APIRouter, status

from app.common.annotations import DatabaseSession
from app.user import services
from app.user.annotations import CurrentUser
from app.user.formatters import format_user
from app.user.schemas import edit, response

# Globals
router = APIRouter()


@router.patch(
    "/setup",
    summary="Setup User Account",
    response_description="The user's details",
    status_code=status.HTTP_200_OK,
    response_model=response.UserResponse,
)
async def route_user_set(
    account_type: Literal["INDIVIDUAL", "PRACTITIONER"],
    user_in: edit.UserEdit,
    curr_user: CurrentUser,
    db: DatabaseSession,
):
    """
    This endpoints edits the user's details
    """

    user = await services.set_user(
        user=curr_user, account_type=account_type, data=user_in, db=db
    )

    return {"data": await format_user(user=user)}
