from loguru import logger

from configs.api import ApiConfig

version = ApiConfig().VERSION

match version:
    case "1":
        from api.v1.app import create_app

        app = create_app()

        logger.info(f"API version: {version}")
    case _:
        raise ValueError(f"Invalid API version: {version}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
