from fastapi import APIRouter

from .network import network_router

assets_router = APIRouter()
assets_router.include_router(network_router, prefix="/network", tags=["assets"])
