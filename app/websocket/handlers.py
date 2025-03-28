from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.medchat import selectors as medchat_selectors
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


async def handle_medchat_interaction(
    ws: WebSocket,
    user: user_models.User,
    data: mc_schemas.WsMedChatInteraction,
    db: AsyncSession,
):
    """
    Handler for medchat-interaction
    """

    # Get medchat
    medchat = await medchat_selectors.get_medchat_by_id(
        id=data.chat_id, db=db, raise_exc=False
    )
    if not medchat:
        await ws.send_json({"type": "error", "data": {"msg": "MedChat Not Found"}})
        return

    # Check: ownership
    if medchat.user_id != user.id:  # type: ignore
        await ws.send_json(
            {
                "type": "error",
                "data": {"msg": "You are not allowed to access this chat"},
            }
        )
        return

    # Form messages
    messages = [
        {
            "role": "system",
            "content": MEDCHAT_SYS_PROMPT,
        },
    ]
    messages.extend(
        [{"role": msg.sender, "content": msg.content} for msg in medchat.messages]  # type: ignore
    )
    messages.append(
        {
            "role": "user",
            "content": data.content,
        }
    )

    # Stream response
    sys_resp = oai_client.chat.completions.create(
        messages=messages,  # type: ignore
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

    # Form full title
    resp = "".join(response_chunks)

    # Save texts
    await medchat_services.create_message(
        medchat=medchat, sender="user", data=data, db=db
    )
    sys_msg = await medchat_services.create_message(
        medchat=medchat,
        sender="system",
        data=mc_schemas.MedChatMessageCreate(type="text", content=resp),
        db=db,
    )

    # Send complete msg
    await ws.send_json(
        data=jsonable_encoder(
            {
                "type": wsresp.medchatmsg_stream_comp,
                "data": {"chat_id": medchat.id, "msg_id": sys_msg.id, "content": resp},
            }
        )
    )

    return
