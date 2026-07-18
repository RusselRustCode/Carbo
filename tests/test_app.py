# import os
# import uuid
# from datetime import date, timedelta
# import importlib
# import pytest
# from fastapi import FastAPI
# import asyncio
# from app.core.database import AsyncSessionLocal
# from fastapi.testclient import TestClient
# from sqlalchemy import text
# from sqlalchemy.exc import IntegrityError
# from dotenv import load_dotenv
# from app.core.database import engine

# load_dotenv()
# DATABASE_URL = os.environ.get('DATABASE_URL')

# pytestmark = pytest.mark.skipif(not DATABASE_URL, reason='DATABASE_URL not set; integration tests skipped')


# def test_app_imports():
#     mod = importlib.import_module('app.main')
#     assert hasattr(mod, 'app')
#     assert isinstance(mod.app, FastAPI)


# def create_employee(client):
#     email = f'user-{uuid.uuid4().hex[:8]}@example.com'
#     payload = {'full_name': 'Test Employee', 'email': email}
#     resp = client.post('/api/v1/employees/', json=payload)
#     resp.raise_for_status()
#     return resp.json()


# def create_group(client):
#     payload = {'name': 'Test Group', 'description': 'Integration test group'}
#     resp = client.post('/api/v1/research-groups/', json=payload)
#     resp.raise_for_status()
#     return resp.json()


# def add_group_member(client, group_id, employee_id):
#     payload = {'employee_id': employee_id, 'role': 'researcher', 'status': 'active'}
#     resp = client.post(f'/api/v1/research-groups/{group_id}/members', json=payload)
#     resp.raise_for_status()
#     return resp.json()


# def create_task(client, responsible_member_id, deadline_at):
#     payload = {
#         'title': 'Task for overdue test',
#         'description': 'Task description',
#         'responsible_member_id': responsible_member_id,
#         'deadline_at': deadline_at,
#         'status': 'todo',
#         'priority': 'normal',
#     }
#     resp = client.post('/api/v1/tasks', json=payload)
#     resp.raise_for_status()
#     return resp.json()


# def get_audit_entries(client, entity_type, entity_id):
#     resp = client.get(f'/api/v1/audit-log?entity_type={entity_type}&entity_id={entity_id}')
#     resp.raise_for_status()
#     return resp.json()


# def test_task_overdue_cycle_and_audit():
#     from app.main import app

#     with TestClient(app) as client:
#         group = create_group(client)
#         employee = create_employee(client)
#         member = add_group_member(client, group['id'], employee['id'])

#         tomorrow = (date.today() + timedelta(days=1)).isoformat()
#         task = create_task(client, member['id'], tomorrow)
#         assert task['is_overdue'] is False

#         yesterday = (date.today() - timedelta(days=1)).isoformat()
#         resp = client.patch(f"/api/v1/tasks/{task['id']}", json={'deadline_at': yesterday})
#         resp.raise_for_status()
#         task_after_deadline = resp.json()
#         assert task_after_deadline['is_overdue'] is True

#         bad_resp = client.patch(f"/api/v1/tasks/{task['id']}", json={'status': 'done'})
#         assert bad_resp.status_code == 400

#         employee2 = create_employee(client)
#         member2 = add_group_member(client, group['id'], employee2['id'])
#         resp = client.patch(
#             f"/api/v1/tasks/{task['id']}",
#             json={'responsible_member_id': member2['id']},
#         )
#         resp.raise_for_status()
#         updated_task = resp.json()
#         assert updated_task['responsible_member_id'] == member2['id']

#         audit_entries = get_audit_entries(client, 'task', task['id'])
#         assignee_changes = [entry for entry in audit_entries if entry['action'] == 'assignee_changed']
#         assert assignee_changes, 'Expected assignee_changed audit entry'
#         assert any(
#             entry['old_value'].get('responsible_member_id') == member['id']
#             and entry['new_value'].get('responsible_member_id') == member2['id']
#             for entry in assignee_changes
#         )

#     # perform an async delete check to avoid sync engine greenlet issues
#     async def _attempt_delete(member_id: str):
#         async with AsyncSessionLocal() as session:
#             try:
#                 await session.execute(text('DELETE FROM group_members WHERE id = :id'), {'id': member_id})
#                 await session.commit()
#             except IntegrityError:
#                 await session.rollback()
#                 raise

#     with pytest.raises(IntegrityError):
#         asyncio.run(_attempt_delete(member['id']))
