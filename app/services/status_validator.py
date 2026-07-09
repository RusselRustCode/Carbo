from enum import Enum
from typing import Dict, List
from fastapi import HTTPException
from app.models.enums import TaskStatus, WorkStatus

TRANSITIONS: Dict[Enum, List[Enum]] = {
    TaskStatus.todo: [TaskStatus.in_progress, TaskStatus.cancelled],
    TaskStatus.in_progress: [TaskStatus.blocked, TaskStatus.done, TaskStatus.cancelled],
    TaskStatus.blocked: [TaskStatus.in_progress, TaskStatus.cancelled],
    TaskStatus.done: [TaskStatus.todo],
    TaskStatus.cancelled: [TaskStatus.todo],
    WorkStatus.todo: [WorkStatus.in_progress, WorkStatus.cancelled],
    WorkStatus.in_progress: [WorkStatus.blocked, WorkStatus.done, WorkStatus.cancelled],
    WorkStatus.blocked: [WorkStatus.in_progress, WorkStatus.cancelled],
    WorkStatus.done: [WorkStatus.todo],
    WorkStatus.cancelled: [WorkStatus.todo],
}


def validate_transition(old: Enum, new: Enum) -> bool:
    if old == new:
        return True
    allowed = TRANSITIONS.get(old, [])
    if new not in allowed:
        raise HTTPException(status_code=400, detail="Invalid status transition")
    return True
