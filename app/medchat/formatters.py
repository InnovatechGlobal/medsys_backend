from app.medchat import models


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
        "attachment_url": msg.attachment_url,
        "attachment_name": msg.attachment_name,
        "attachment_type": msg.attachment_type,
        "created_at": msg.created_at,
    }
