from fastapi import APIRouter

from .process import process_router

ml_router = APIRouter()
ml_router.include_router(process_router, prefix="/process", tags=["ml"])
