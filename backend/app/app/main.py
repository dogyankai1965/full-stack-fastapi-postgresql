from typing import Any
from fastapi import Depends, FastAPI
from fastapi_simple_security import api_key_router, api_key_security
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

app.include_router(api_key_router, prefix="/auth", tags=["_auth"])


@app.get("/secure", dependencies=[Depends(api_key_security)])
def secure_endpoint() -> Any:
    return {"message": "This is a secure endpoint"}
