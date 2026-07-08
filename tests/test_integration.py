import os
import pytest
import asyncio
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DATABASE_URL not set; integration tests skipped")

def test_placeholder():
    # Placeholder to ensure pytest runs at least one DB test when DB is configured.
    assert True
