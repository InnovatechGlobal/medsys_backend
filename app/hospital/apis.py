from fastapi import APIRouter

from app.core.tags import get_tags
from app.hospital.routes.base import router as base_router

# Globals
router = APIRouter()
tags = get_tags()

# Routers
router.include_router(base_router, prefix="/hospital", tags=[tags.HOSPITAL])
