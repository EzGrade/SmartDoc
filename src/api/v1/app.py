from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import v1_router


@asynccontextmanager
async def lifespan_event(app: FastAPI):
    yield


def create_app():
    app = FastAPI(
        lifespan=lifespan_event,
        root_path="/api/v1",
        swaggers_ui_parameters={"deepLinking": True},
        openapi_url="/openapi.json",
    )
    app.include_router(v1_router)
    return app
