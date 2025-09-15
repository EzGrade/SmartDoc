from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.v1.schemas.system.health import HealthResponseSchema

router = APIRouter()


@router.get("/health", response_model=HealthResponseSchema)
async def health():
    return JSONResponse(
        status_code=200,
        content=HealthResponseSchema().model_dump(),
    )
