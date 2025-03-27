from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.medchat import services as medchat_services
from app.medchat.prompts import MEDCHAT_SYS_PROMPT, MEDCHAT_TITLE_PROMPT
from app.medchat.schemas import create as mc_schemas
from app.user import models as user_models
from app.websocket.types import WSResponseTypes

# Globals
settings = get_settings()
oai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
wsresp = WSResponseTypes()


async def handle_medchat_create(
    ws: WebSocket,
    user: user_models.User,
    data: mc_schemas.WsMedChatCreate,
    db: AsyncSession,
):
    """
    Handler for medchat-create events
    """

    # Create medchat
    medchat = await medchat_services.create_medchat(user=user, db=db)

    # Generate response
    sys_resp = oai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": MEDCHAT_SYS_PROMPT},
            {"role": "user", "content": data.content},
        ],
        model="gpt-4o",
        stream=True,
    )
    response_chunks = []
    for chunk in sys_resp:
        content = chunk.choices[0].delta.content
        if content:
            response_chunks.append(content)
            await ws.send_json(
                data=jsonable_encoder(
                    {
                        "type": wsresp.medchatmsg_stream,
                        "data": {"chat_id": medchat.id, "content": content},
                    }
                )
            )

    # Send full stream
    resp = "".join(response_chunks)
    await ws.send_json(
        data=jsonable_encoder(
            {
                "type": wsresp.medchatmsg_stream_comp,
                "data": {"chat_id": medchat.id, "content": resp},
            }
        )
    )

    # Create message
    await medchat_services.create_message(
        medchat=medchat, sender="system", data=data, db=db
    )

    # Stream title
    sys_resp = oai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": MEDCHAT_TITLE_PROMPT.format(msg=data.content),
            },
        ],
        model="gpt-4o",
        stream=True,
    )
    response_chunks = []
    for chunk in sys_resp:
        content = chunk.choices[0].delta.content
        if content:
            response_chunks.append(content)
            await ws.send_json(
                data=jsonable_encoder(
                    {
                        "type": wsresp.medchattitle_stream,
                        "data": {"chat_id": medchat.id, "content": content},
                    }
                )
            )

    # Form full title
    title = "".join(response_chunks)
    await ws.send_json(
        data=jsonable_encoder(
            {
                "type": wsresp.medchattitle_stream_comp,
                "data": {"chat_id": medchat.id, "content": title},
            }
        )
    )

    # Save title
    setattr(medchat, "title", title)
    await db.commit()

    return medchat
