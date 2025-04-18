import os
from datetime import datetime

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils import (
    extract_text_from_docx,
    extract_text_from_pdf,
    trim_text_to_token_limit,
)
from app.core.settings import get_settings
from app.medchat import selectors as medchat_selectors
from app.medchat import services as medchat_services
from app.medchat.prompts import (
    MEDCHAT_ATTACHMENT_CONTENT_PROMPT,
    MEDCHAT_SYS_PROMPT,
)
from app.medchat.schemas import create as mc_schemas
from app.user import models as user_models
from app.websocket import schemas, utils
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
    medchat = await medchat_services.create_medchat(
        user=user, patient_id=data.patient_id, db=db
    )

    # Form context prompt
    context_prompt = f"Use the below patient details to answer related questions:\n{medchat.patient_context}"

    # Create patient context message
    await medchat_services.create_message(
        medchat=medchat,
        sender="system",
        data=mc_schemas.MedChatMessageCreate(
            type="text", content=context_prompt, attachment=None
        ),
        db=db,
        hidden=True,
    )

    # Check: attachment
    text_content = None
    attachment_prompt = None
    attachment_details = None
    if data.attachment:
        # Decode base6
        filepath = await utils.save_base64_file(
            base64_str=data.attachment.file_content, file_type=data.attachment.file_type
        )

        # Read document
        if data.attachment.file_type == "pdf":
            text_content = await extract_text_from_pdf(filepath=filepath)
        else:
            text_content = await extract_text_from_docx(filepath=filepath)

        # Check: valid medical
        resp = oai_client.beta.chat.completions.parse(
            messages=[
                {"role": "system", "content": MEDCHAT_ATTACHMENT_CONTENT_PROMPT},
                {"role": "user", "content": text_content},
            ],
            model="gpt-4o",
            response_format=schemas.MedChatAttachmentContentCheck,
        )
        if not resp.choices[0].message.parsed.is_valid:  # type: ignore
            await ws.send_json(
                {
                    "type": "validation-error",
                    "data": {
                        "msg": "Contents of the attachment is not a medical document or medical related"
                    },
                }
            )

            # Delete medchat
            await db.delete(medchat)
            await db.commit()

            return

        # Update prompt
        attachment_prompt = f"Use the below information to answer the following questions if related:\n{text_content}"

        # Create attachment_details
        attachment_details = {}
        attachment_details["attachment_url"] = filepath
        attachment_details["attachment_name"] = os.path.basename(filepath)
        attachment_details["attachment_type"] = data.attachment.file_type
        attachment_details["attachment_content"] = text_content

    # Generate response
    sys_resp = oai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": MEDCHAT_SYS_PROMPT},
            {"role": "system", "content": context_prompt},
            {
                "role": "system",
                "content": attachment_prompt if attachment_prompt else "",
            },
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
                "data": {
                    "chat_id": medchat.id,
                    "content": resp,
                    "attachment": {
                        "attachment_url": settings.MEDIA_URL + "/" + filepath,
                        "attachment_name": os.path.basename(filepath),
                        "attachment_type": data.attachment.file_type,
                    }
                    if data.attachment
                    else None,
                },
            }
        )
    )

    # Save user msg
    await medchat_services.create_message(
        medchat=medchat,
        sender="user",
        data=data,
        db=db,
        attachment=mc_schemas.InternalMedChatAttachmentCreate(**attachment_details)
        if attachment_details
        else None,
    )

    # Create hidden message for attachment prompt
    if attachment_prompt:
        await medchat_services.create_message(
            medchat=medchat,
            sender="system",
            data=mc_schemas.MedChatMessageCreate(
                type="text", content=attachment_prompt, attachment=None
            ),
            hidden=True,
            db=db,
        )

    # Create sys emsage
    await medchat_services.create_message(
        medchat=medchat,
        sender="system",
        data=mc_schemas.MedChatMessageCreate(type="text", content=resp),
        db=db,
    )

    # Save title
    setattr(medchat, "title", f"Medchat - {data.patient_id}")
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

    # Update: updated_at
    setattr(medchat, "updated_at", datetime.now())
    await db.commit()

    # Check: attachment
    text_content = None
    attachment_prompt = None
    attachment_details = None
    if data.attachment:
        # Decode base6
        filepath = await utils.save_base64_file(
            base64_str=data.attachment.file_content, file_type=data.attachment.file_type
        )

        # Read document
        if data.attachment.file_type == "pdf":
            text_content = await extract_text_from_pdf(filepath=filepath)
        else:
            text_content = await extract_text_from_docx(filepath=filepath)

        # Update prompt
        attachment_prompt = (
            "Use the below information to answer the following questions if related:\n"
            f"{await trim_text_to_token_limit(text_content)}"
        )

        # Create attachment_details
        attachment_details = {}
        attachment_details["attachment_url"] = filepath
        attachment_details["attachment_name"] = os.path.basename(filepath)
        attachment_details["attachment_type"] = data.attachment.file_type
        attachment_details["attachment_content"] = text_content

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

    # Add attachment prompt
    if attachment_prompt:
        messages.append(
            {
                "role": "system",
                "content": attachment_prompt,
            }
        )

    # Add user msg
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

    # Save user msg
    await medchat_services.create_message(
        medchat=medchat,
        sender="user",
        data=data,
        db=db,
        attachment=mc_schemas.InternalMedChatAttachmentCreate(**attachment_details)
        if attachment_details
        else None,
    )

    # Create hidden message for attachment prompt
    if attachment_prompt:
        await medchat_services.create_message(
            medchat=medchat,
            sender="system",
            data=mc_schemas.MedChatMessageCreate(
                type="text", content=attachment_prompt, attachment=None
            ),
            hidden=True,
            db=db,
        )

    sys_msg = await medchat_services.create_message(
        medchat=medchat,
        sender="system",
        data=mc_schemas.MedChatMessageCreate(type="text", content=resp),
        db=db,
    )

    # Send full stream
    resp = "".join(response_chunks)
    await ws.send_json(
        data=jsonable_encoder(
            {
                "type": wsresp.medchatmsg_stream_comp,
                "data": {
                    "chat_id": medchat.id,
                    "msg_id": sys_msg.id,
                    "content": resp,
                    "attachment": {
                        "attachment_url": settings.MEDIA_URL + "/" + filepath,
                        "attachment_name": os.path.basename(filepath),
                        "attachment_type": data.attachment.file_type,
                    }
                    if data.attachment
                    else None,
                },
            }
        )
    )

    return
