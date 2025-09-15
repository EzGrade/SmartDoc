from fastapi import APIRouter

from api.v1.endpoints.assets import assets_router
from api.v1.endpoints.ml import ml_router
from api.v1.endpoints.system import system_router

v1_router = APIRouter()
v1_router.include_router(system_router, prefix="/system", tags=["system"])
v1_router.include_router(assets_router, prefix="/assets", tags=["assets"])
v1_router.include_router(ml_router, prefix="/ml", tags=["ml"])
