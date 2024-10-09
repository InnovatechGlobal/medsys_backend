from fastapi import APIRouter

from app.user.routes.base import router as base_router

# Globals
router = APIRouter()

# Include routes
router.include_router(base_router, prefix="/user")
