# app/services/s3_storage.py
import asyncio
from functools import partial
from typing import Optional
from data_pipeline.s3_client import S3Storage
from data_pipeline.config import data_settings

class AsyncS3Storage:
    """Асинхронная обертка над синхронным S3Storage для использования в FastAPI."""
    def __init__(self):
        # Просто создаем синхронный клиент, не трогая asyncio
        self._sync_storage = S3Storage()

    async def ensure_bucket(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._sync_storage.ensure_bucket)

    async def upload_file(self, local_path: str, object_key: str) -> str:
        loop = asyncio.get_running_loop()
        func = partial(self._sync_storage.upload_file, local_path, object_key)
        return await loop.run_in_executor(None, func)

    async def upload_bytes(self, data: bytes, object_key: str) -> str:
        loop = asyncio.get_running_loop()
        func = partial(self._sync_storage.upload_bytes, data, object_key)
        return await loop.run_in_executor(None, func)

    async def download_to_buffer(self, object_key: str):
        loop = asyncio.get_running_loop()
        func = partial(self._sync_storage.download_to_buffer, object_key)
        return await loop.run_in_executor(None, func)

# Синглтон для dependency injection
s3_storage = AsyncS3Storage()