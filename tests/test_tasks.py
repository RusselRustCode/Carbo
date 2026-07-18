import pytest
from uuid import uuid4
from datetime import date, timedelta

async def create_test_employee(client):
    payload = {"full_name": "Test User", "email": f"test_{uuid4().hex[:6]}@ex.com"}
    resp = await client.post("/api/v1/employees/", json=payload)
    return resp.json()

async def create_test_group(client):
    payload = {"name": "Test Group", "description": "Desc"}
    resp = await client.post("/api/v1/research-groups/", json=payload)
    return resp.json()

async def prepare_task_context(client):
    emp = await create_test_employee(client)
    grp = await create_test_group(client)
    
    member_resp = await client.post(f"/api/v1/research-groups/{grp['id']}/members", json={
        "employee_id": emp["id"], "role": "lead", "status": "active"
    })
    member_id = member_resp.json()["id"]
    
    task_payload = {
        "title": "Important Task",
        "responsible_member_id": member_id,
        "deadline_at": (date.today() + timedelta(days=5)).isoformat(),
        "priority": "high",
        "status": "todo"
    }
    task_resp = await client.post("/api/v1/tasks", json=task_payload)
    return task_resp.json(), member_id

@pytest.mark.asyncio
async def test_create_and_update_task(client):
    task, _ = await prepare_task_context(client)
    update_payload = {"status": "in_progress"}
    response = await client.patch(f"/api/v1/tasks/{task['id']}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_task_status_validation(client):
    task, _ = await prepare_task_context(client)
    invalid_payload = {"status": "done"}
    response = await client.patch(f"/api/v1/tasks/{task['id']}", json=invalid_payload)
    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]