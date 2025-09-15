from fastapi import APIRouter

from api.v1.endpoints.system.health import router as health_router

system_router = APIRouter()

system_router.include_router(health_router, prefix="/health", tags=["system"])
