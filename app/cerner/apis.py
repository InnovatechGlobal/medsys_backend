from fastapi import APIRouter

from app.cerner.routes.appointment import router as appointment_router
from app.cerner.routes.base import router as base_router
from app.core.tags import RouteTags

# Globals
router = APIRouter()
tags = RouteTags()

# Include routes
router.include_router(base_router, prefix="/cerner")
router.include_router(
    appointment_router, prefix="/cerner/appointments", tags=[tags.CERNER_APPOINTMENT]
)
