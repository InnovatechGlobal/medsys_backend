from app.core.settings import get_settings
from app.medchat import models

# Globals
settings = get_settings()


async def format_medchat(medchat: models.MedChat):
    """
    Format medchat obj to dict
    """

    return {
        "id": medchat.id,
        "title": medchat.title,
        "updated_at": medchat.updated_at,
        "created_at": medchat.created_at,
    }


async def format_medchat_message(msg: models.MedChatMessage):
    """
    Format medchat message to dict
    """

    return {
        "id": msg.id,
        "sender": msg.sender,
        "type": msg.type,
        "content": msg.content,
        "audio_url": msg.audio_url,
        "attachment": {
            "attachment_url": settings.MEDIA_URL + msg.attachment_url,
            "attachment_name": msg.attachment_name,
            "attachment_type": msg.attachment_type,
        }
        if msg.attachment_url  # type: ignore
        else None,
        "created_at": msg.created_at,
    }
