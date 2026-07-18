# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Импортируем приложение под другим именем
from app.main import app as fastapi_app
from app.core.database import get_db
from app.models.base import Base
from app.core.config import settings
import app.models 
from sqlalchemy.pool import NullPool

TEST_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)

AsyncTestingSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autoflush=False
)

async def override_get_db():
    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

fastapi_app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    except Exception:
        pass
    finally:
        await engine.dispose()

@pytest.fixture
async def client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac