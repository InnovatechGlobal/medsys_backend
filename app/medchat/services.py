from typing import Literal

from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.medchat import models
from app.medchat.crud import MedChatCRUD, MedChatMessageCRUD
from app.medchat.schemas import create
from app.user import models as user_models

# Globals
settings = get_settings()
oai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def create_medchat(user: user_models.User, patient_id: str, db: AsyncSession):
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

    # TEMP: get random diagnosis
    sys_resp = oai_client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Generate a random patients medical history"},
        ],
        model="gpt-4o",
    )

    # Create obj
    obj = await medchat_crud.create(
        data={
            "user_id": user.id,
            "title": "Temp Title",
            "patient_id": patient_id,
            "patient_service": "cerner",
            "patient_context": sys_resp.choices[0].message.content,
        }
    )

    return obj


async def create_message(
    medchat: models.MedChat,
    sender: Literal["system", "user"],
    data: create.MedChatMessageCreate,
    db: AsyncSession,
    hidden: bool = False,
    attachment: create.InternalMedChatAttachmentCreate | None = None,
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
    create_data = {
        "chat_id": medchat.id,
        "sender": sender,
        "type": data.type,
        "content": data.content,
        "hidden": hidden,
    }

    # Check: attachment
    if attachment:
        create_data["attachment_url"] = "/" + attachment.attachment_url
        create_data["attachment_name"] = attachment.attachment_name
        create_data["attachment_type"] = attachment.attachment_type
        create_data["attachment_content"] = attachment.attachment_content

    obj = await msg_crud.create(data=create_data)

    return obj
