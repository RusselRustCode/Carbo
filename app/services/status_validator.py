from typing import Dict, List
from app.models.enums import TaskStatus

TRANSITIONS: Dict[TaskStatus, List[TaskStatus]] = {
    TaskStatus.todo: [TaskStatus.in_progress, TaskStatus.cancelled],
    TaskStatus.in_progress: [TaskStatus.blocked, TaskStatus.done, TaskStatus.cancelled],
    TaskStatus.blocked: [TaskStatus.in_progress, TaskStatus.cancelled],
    TaskStatus.done: [TaskStatus.todo],
    TaskStatus.cancelled: [TaskStatus.todo],
}


def validate_transition(old: TaskStatus, new: TaskStatus) -> bool:
    if old == new:
        return True
    allowed = TRANSITIONS.get(old, [])
    return new in allowed
