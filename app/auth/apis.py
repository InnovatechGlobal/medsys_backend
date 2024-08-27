from fastapi import APIRouter

from app.auth.routes.oauth2 import router as oauth2_router

router = APIRouter()

# Include sub routes
router.include_router(oauth2_router, prefix="/oauth2", tags=["Oauth2 Endpoints"])
