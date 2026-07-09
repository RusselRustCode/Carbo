import enum

class GroupStatus(str, enum.Enum):
    active = "active"
    archived = "archived"


class MemberRole(str, enum.Enum):
    lead = "lead"
    researcher = "researcher"
    assistant = "assistant"
    observer = "observer"


class MemberStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    left = "left"


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    done = "done"
    cancelled = "cancelled"


class TaskPriority(str, enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"
    critical = "critical"


class WorkStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    done = "done"
    cancelled = "cancelled"

class AuditAction(str, enum.Enum):
    created = "created"
    updated = "updated"
    status_changed = "status_changed"
    deadline_changed = "deadline_changed"
    assignee_changed = "assignee_changed"
    deleted = "deleted"

class ProjectStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    completed = "completed"
    archived = "archived"


class AccessLevel(str, enum.Enum):
    read = "read"
    write = "write"
    admin = "admin"


class GoalStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    achieved = "achieved"
    cancelled = "cancelled"
