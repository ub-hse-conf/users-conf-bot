from dataclasses import dataclass

from src.models.task.task_status import UserTaskStatus
from src.models.task.user_task_type import UserTaskType


@dataclass
class UserTask:
    id: int
    name: str
    description: str
    is_available: bool
    status: UserTaskStatus
    task_type: UserTaskType
