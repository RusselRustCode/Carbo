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
