from fastapi import APIRouter

from app.medchat.routes.base import router as base_router

# Globals
router = APIRouter()

# Include routes
router.include_router(base_router, prefix="/medchats")
