from fastapi import APIRouter, status

from app.common.annotations import DatabaseSession
from app.common.exceptions import BadRequest
from app.user import services
from app.user.annotations import CurrentUser
from app.user.formatters import format_user
from app.user.schemas import edit, response

# Globals
router = APIRouter()


@router.post(
    "/setup",
    summary="Setup User Account",
    response_description="The user's details",
    status_code=status.HTTP_200_OK,
    response_model=response.UserResponse,
)
async def route_user_setup(
    setup_in: edit.UserAccountSetup,
    curr_user: CurrentUser,
    db: DatabaseSession,
):
    """
    This endpoints edits the user's details
    """

    # Check: user is already setup
    if curr_user.account_type:  # type: ignore
        raise BadRequest("You have already setup your account")

    user = await services.setup_user_account(user=curr_user, data=setup_in, db=db)

    return {"data": await format_user(user=user)}
