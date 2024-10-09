from fastapi import APIRouter

from app.auth.routes.oauth2 import router as oauth2_router
from app.core.tags import get_tags

# Globals
router = APIRouter()
tags = get_tags()

# Include sub routes
router.include_router(oauth2_router, prefix="/oauth2", tags=[tags.OAUTH2_ENDPOINT])
