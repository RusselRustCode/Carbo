import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_employee(client):
    payload = {
        "full_name": "John Doe",
        "email": f"john_{uuid4().hex[:6]}@example.com"
    }
    response = await client.post("/api/v1/employees/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_employee_duplicate_email(client):
    email = f"unique_{uuid4().hex[:6]}@example.com"
    payload = {"full_name": "Jane Doe", "email": email}
    
    await client.post("/api/v1/employees/", json=payload)
    
    response = await client.post("/api/v1/employees/", json=payload)
    assert response.status_code in [409, 400, 422] 