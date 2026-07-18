import pytest
from uuid import uuid4

async def create_test_employee(client):
    payload = {"full_name": "Test User", "email": f"test_{uuid4().hex[:6]}@ex.com"}
    resp = await client.post("/api/v1/employees/", json=payload)
    return resp.json()

async def create_test_group(client):
    payload = {"name": "Test Group", "description": "Desc"}
    resp = await client.post("/api/v1/research-groups/", json=payload)
    return resp.json()

@pytest.mark.asyncio
async def test_add_member_to_group(client):
    employee = await create_test_employee(client)
    group = await create_test_group(client)
    
    member_payload = {
        "employee_id": employee["id"],
        "role": "researcher",
        "status": "active"
    }
    
    response = await client.post(f"/api/v1/research-groups/{group['id']}/members", json=member_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee["id"]