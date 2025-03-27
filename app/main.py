from contextlib import asynccontextmanager

from anyio import to_thread
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from app.auth.apis import router as auth_router
from app.cerner.apis import router as cerner_router
from app.common.dependencies import get_session
from app.common.exceptions import (
    BadGatewayError,
    CustomHTTPException,
    InternalServerError,
)
from app.core.handlers import (
    bad_gateway_error_exception_handler,
    base_exception_handler,
    custom_http_exception_handler,
    internal_server_error_exception_handler,
    request_validation_exception_handler,
)
from app.core.tags import get_tags
from app.hospital.apis import router as hospital_router
from app.user.apis import router as user_router
from app.websocket.route import router as ws_router

# Globals
tags = get_tags()


# Lifespan (startup, shutdown)
@asynccontextmanager
async def lifespan(_: FastAPI):
    """This is the startup and shutdown code for the FastAPI application."""
    # Startup code
    print("Starting Server...")

    # Bigger Threadpool i.e you send a bunch of requests it will handle a max of 1000 at a time, the default is 40 # pylint: disable=line-too-long
    limiter = to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000

    # Shutdown Code
    yield
    print("Shutting Down Server...")


app = FastAPI(
    title="Behemoth FastAPI",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url="/",
    contact={
        "name": "GrandGale Technologies",
        "url": "https://github.com/GrandGaleTechnologies",
        "email": "angobello0@gmail.com",
    },
)

# Allowed Origins
origins = ["*"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    GZipMiddleware,
    minimum_size=5000,  # Minimum size of the response before it is compressed in bytes
)


# Exception Handlers
app.add_exception_handler(Exception, base_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore
app.add_exception_handler(InternalServerError, internal_server_error_exception_handler)  # type: ignore
app.add_exception_handler(BadGatewayError, bad_gateway_error_exception_handler)  # type: ignore
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)  # type: ignore


# Healthcheck
@app.get("/health", include_in_schema=False)
async def health(_: Session = Depends(get_session)):
    """App Healthcheck"""
    return {"status": "Ok!"}


# Routers
app.include_router(ws_router, tags=["Websocket"])
app.include_router(auth_router, prefix="/auth", tags=[tags.AUTH])
app.include_router(user_router, tags=[tags.USER])
app.include_router(hospital_router, tags=[tags.HOSPITAL])
app.include_router(cerner_router, tags=[tags.CERNER])
