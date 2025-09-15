from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse

from api.v1.dependencies.core.services.file_system import get_file_system_aggregator
from api.v1.schemas.assets.network import NetworkUploadAssetSchema
from core.services.file_system.aggregator import FSAggregator
from shared.enums.services.core.file_system import FSProvidersEnum

network_router = APIRouter()


@network_router.post("/upload", response_model=NetworkUploadAssetSchema)
async def network(
        file_system_aggregator: Annotated[FSAggregator, Depends(get_file_system_aggregator)],
        file: UploadFile = File(...),
):
    await file_system_aggregator.write(
        provider=FSProvidersEnum.S3,
        path=file.filename,
        data=await file.read(),
    )
    return JSONResponse(
        status_code=200,
        content=NetworkUploadAssetSchema(uuid=str(uuid4())).model_dump(),
    )
