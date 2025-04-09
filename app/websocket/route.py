import jwt
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
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
        curr_user = await user_selectors.get_current_ws_user(ws=ws, token=token, db=db)
    except (
        Unauthorized,
        HTTPException,
        jwt.exceptions.ExpiredSignatureError,
        jwt.PyJWTError,
        jwt.exceptions.InvalidSignatureError,
    ) as e:
        if isinstance(e, Unauthorized):
            error_msg = e.msg
        elif isinstance(e, HTTPException):
            error_msg = e.detail
        else:
            error_msg = str(e)

        await ws.send_json({"type": "auth-error", "data": {"msg": error_msg}})
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

            # Handler: chat-create
            if payload.type == "medchat-create":
                # Validate base payload
                try:
                    data = mc_schemas.WsMedChatCreate.model_validate(payload.data)
                except ValidationError as e:
                    errors = e.errors()
                    for err in errors:
                        if "ctx" in err and "error" in err["ctx"]:
                            err["ctx"]["error"] = str(
                                err["ctx"]["error"]
                            )  # Convert to string
                    await ws.send_json(
                        {
                            "type": "validation-error",
                            "data": {
                                "msg": "Invalid medchat-create payload",
                                "errors": errors,
                            },
                        }
                    )
                    await ws.close(code=4000, reason="Invalid Payload")
                    return

                # Handle event
                await handlers.handle_medchat_create(
                    ws=ws, user=curr_user, data=data, db=db
                )

            # Handler: medchat-interaction
            elif payload.type == "medchat-interaction":
                # Validate base payload
                try:
                    data = mc_schemas.WsMedChatInteraction.model_validate(payload.data)
                except ValidationError as e:
                    await ws.send_json(
                        {
                            "type": "validation-error",
                            "data": {
                                "msg": "Invalid medchat-interaction payload",
                                "errors": e.errors(),
                            },
                        }
                    )
                    await ws.close(code=4000, reason="Invalid Payload")
                    return

                # Handle event
                await handlers.handle_medchat_interaction(
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
        if isinstance(e, Exception):
            raise e

    finally:
        # Always close the database session at the end of the connection
        await db.close()
