from fastapi import APIRouter

from api.v1.schemas.assets.network import NetworkUploadAssetSchema

process_router = APIRouter()


@process_router.post("/process", response_model=NetworkUploadAssetSchema)
async def process():
    ...
