import os
import pytest
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DATABASE_URL not set; integration tests skipped")

@pytest.mark.asyncio
async def test_placeholder(client):
    response = await client.get("/api/v1/projects", follow_redirects=True)
    assert response.status_code == 200