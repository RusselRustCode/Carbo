import asyncio
from functools import partial
from typing import Optional
from data_pipeline.s3_client import S3Storage
from data_pipeline.config import data_settings


class AsyncS3Storage:
    """Асинхронная обертка над синхронным S3Storage для использования в FastAPI."""

    def __init__(self):
        self._sync_storage = S3Storage()
        self._loop = asyncio.get_event_loop()

    async def ensure_bucket(self) -> None:
        await self._loop.run_in_executor(None, self._sync_storage.ensure_bucket)

    async def upload_file(self, local_path: str, object_key: str) -> str:
        func = partial(self._sync_storage.upload_file, local_path, object_key)
        return await self._loop.run_in_executor(None, func)

    async def upload_bytes(self, data: bytes, object_key: str) -> str:
        func = partial(self._sync_storage.upload_bytes, data, object_key)
        return await self._loop.run_in_executor(None, func)

    async def download_to_buffer(self, object_key: str):
        func = partial(self._sync_storage.download_to_buffer, object_key)
        return await self._loop.run_in_executor(None, func)


# Синглтон для dependency injection
s3_storage = AsyncS3Storage()