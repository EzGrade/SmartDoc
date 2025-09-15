from functools import wraps
from loguru import logger

from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError


def handle_s3_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            logger.error(f"AWS ClientError in {func.__name__}: {error_code} - {e}")
            raise
        except NoCredentialsError:
            logger.error(f"AWS credentials not found in {func.__name__}.")
            raise
        except EndpointConnectionError:
            logger.error(f"Could not connect to the AWS endpoint in {func.__name__}.")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise

    return wrapper
