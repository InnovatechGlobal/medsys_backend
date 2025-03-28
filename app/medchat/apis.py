from fastapi import APIRouter

from app.medchat.routes.base import router as base_router
from app.medchat.routes.message import router as message_router

# Globals
router = APIRouter()

# Include routes
router.include_router(base_router, prefix="/medchats")
router.include_router(message_router, prefix="/medchats/messages")
