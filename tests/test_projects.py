import pytest

@pytest.mark.asyncio
async def test_create_project(client):
    payload = {
        "name": "Test Project",
        "description": "Integration test",
        "status": "planning"
    }
    response = await client.post("/api/v1/projects", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    return data["id"]

@pytest.mark.asyncio
async def test_get_project(client):
    project_id = await test_create_project(client)
    
    response = await client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id

@pytest.mark.asyncio
async def test_delete_project(client):
    project_id = await test_create_project(client)
    
    response = await client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    
    response = await client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 404