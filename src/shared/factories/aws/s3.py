from contextlib import asynccontextmanager
from typing import Optional

import aioboto3
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from botocore.config import Config
from mypy_boto3_cloudwatch.client import CloudWatchClient

from configs.aws.s3 import AwsEnvConfig

AWS_ERROR = "AWS session is not initialized."


class AwsClientFactory:
    def __init__(self, aws_env_config: AwsEnvConfig) -> None:
        self.aws_env_config = aws_env_config
        self.http_session: Optional[ClientSession] = None
        self.aws_config: Config = Config(
            region_name=self.aws_env_config.TARGET_REGION,
            retries={"max_attempts": 1, "mode": "standard"},
        )
        self.session: Optional[aioboto3.Session] = None

    async def initialize_http_session(self) -> None:
        """Initialize an async HTTP session."""
        self.http_session = ClientSession(
            timeout=ClientTimeout(total=30), connector=TCPConnector(limit=50)
        )

    async def initialize_aws_session(self) -> None:
        """Initialize an async AWS session."""
        profile = (
            self.aws_env_config.PROFILE.strip() if self.aws_env_config.PROFILE else None
        )
        access_key = (
            self.aws_env_config.ACCESS_KEY_ID.strip()
            if self.aws_env_config.ACCESS_KEY_ID
            else None
        )
        secret_key = (
            self.aws_env_config.SECRET_ACCESS_KEY.strip()
            if self.aws_env_config.SECRET_ACCESS_KEY
            else None
        )

        # If profile is set and non-empty, use it
        if profile:
            self.session = aioboto3.Session(profile_name=profile)
        # If both access_key and secret_key are provided, use them
        elif access_key and secret_key:
            self.session = aioboto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=self.aws_env_config.TARGET_REGION,
            )
        else:
            # No profile, access_key, or secret_key: use IAM role of the instance directly
            self.session = aioboto3.Session()

    async def get_cloudwatch_client(self) -> CloudWatchClient:
        """Initialize and return an async CloudWatch client."""
        if not self.session:
            await self.initialize_aws_session()

        if self.session:
            # Remove async with and just directly create the client
            return await self.session.client(
                "cloudwatch", config=self.aws_config
            ).__aenter__()
        else:
            raise ValueError(AWS_ERROR)

    @asynccontextmanager
    async def get_s3_client(self):
        if not self.session:
            await self.initialize_aws_session()

        if self.session:
            async with self.session.client("s3", config=self.aws_config) as client:
                yield client
        else:
            raise ValueError(AWS_ERROR)

    async def close_http_session(self) -> None:
        """Close the async HTTP session if it's open."""
        if self.http_session:
            await self.http_session.close()
