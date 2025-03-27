from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from websockets import ConnectionClosedError, ConnectionClosedOK

from app.common.annotations import DatabaseSession
from app.common.exceptions import Unauthorized
from app.medchat.schemas import create as mc_schemas
from app.user import selectors as user_selectors
from app.websocket import handlers, schemas

# Globals
router = APIRouter()


@router.websocket(
    "/ws",
    name="Innovatech WS",
)
async def ws_chat(ws: WebSocket, token: str, db: DatabaseSession):
    """
    Websocket for medical chat
    """

    # Accept conn
    await ws.accept()

    # Check: valid user
    try:
        curr_user = await user_selectors.get_current_ws_user(token=token, db=db)
    except Unauthorized as e:
        await ws.send_json({"type": "auth-error", "data": {"msg": e.msg}})
        await ws.close(code=4001, reason="Auth failure")
        return

    await ws.send_json({"type": "internal", "data": {"msg": "Connection successful"}})

    try:
        while True:
            # Accept req
            data = await ws.receive_json()

            # Validate base payload
            try:
                payload = schemas.BaseInputPayload(**data)
            except ValidationError as e:
                await ws.send_json({"type": "validation-error", "data": e.json()})
                await ws.close(code=4000, reason="Invalid Payload")
                return

            # Handler for chat-create
            if payload.type == "medchat-create":
                # Validate base payload
                try:
                    data = mc_schemas.WsMedChatCreate.model_validate(payload.data)
                except ValidationError as e:
                    await ws.send_json(
                        {
                            "type": "validation-error",
                            "data": {
                                "msg": "Invalid chat-create payload",
                                "errors": e.errors(),
                            },
                        }
                    )
                    await ws.close(code=4000, reason="Invalid Payload")
                    return

                # Handle event
                await handlers.handle_medchat_create(
                    ws=ws, user=curr_user, data=data, db=db
                )

            # Handle invalid payload type
            else:
                await ws.send_json(
                    {
                        "type": "error",
                        "data": {"msg": f"Invalid payload type {data.type}"},
                    }
                )
                await ws.close(code=4000, reason="Invalid Payload")
                return

    except (
        Exception,
        WebSocketDisconnect,
        ConnectionClosedError,
        ConnectionClosedOK,
    ) as e:
        raise e

    finally:
        # Always close the database session at the end of the connection
        await db.close()
