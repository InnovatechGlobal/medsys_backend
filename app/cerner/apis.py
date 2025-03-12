from fastapi import APIRouter

from app.cerner.routes.appointment import router as appointment_router
from app.cerner.routes.base import router as base_router
from app.cerner.routes.patient import router as patient_router
from app.core.tags import RouteTags

# Globals
router = APIRouter()
tags = RouteTags()

# Include routes
router.include_router(base_router, prefix="/cerner")
router.include_router(
    appointment_router, prefix="/cerner/appointments", tags=[tags.CERNER_APPOINTMENT]
)
router.include_router(
    patient_router, prefix="/cerner/patients", tags=[tags.CERNER_PATIENT]
)
