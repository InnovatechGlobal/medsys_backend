from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from app.medchat import models
from app.medchat.crud import MedChatCRUD, MedChatMessageCRUD
from app.medchat.schemas import create
from app.user import models as user_models


async def create_medchat(user: user_models.User, db: AsyncSession):
    """
    Create medchats

    Args:
        user (user_models.User): The user obj
        db (AsyncSession): The database session

    Returns:
        models.MedChat: The created medchat obj
    """
    # Init crud
    medchat_crud = MedChatCRUD(db=db)

    # Create obj
    obj = await medchat_crud.create(data={"user_id": user.id, "title": "Temp Title"})

    return obj


async def create_message(
    medchat: models.MedChat,
    sender: Literal["system", "user"],
    data: create.MedChatMessageCreate,
    db: AsyncSession,
):
    """
    Create medchat message

    Args:
        medchat (models.MedChat): The medchat obj
        sender ('system' or 'user'): The sender of the message
        data (create.MedChatMessageCreate): The create schema
        db (AsyncSession): The database session

    Returns:
        models.MedChatMessage: The created message obj
    """
    # Init crud
    msg_crud = MedChatMessageCRUD(db=db)

    # Create msg
    obj = await msg_crud.create(
        data={
            "chat_id": medchat.id,
            "sender": sender,
            "type": data.type,
            "content": data.content,
        }
    )

    return obj
