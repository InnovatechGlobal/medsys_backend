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
