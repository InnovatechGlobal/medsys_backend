from fastapi import APIRouter, WebSocket

from app.common.annotations import DatabaseSession


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
