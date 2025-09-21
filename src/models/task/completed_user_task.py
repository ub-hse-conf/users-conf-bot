from dataclasses import dataclass

from src.models.task.task_status import UserTaskStatus
from src.models.task.user_task_type import UserTaskType


@dataclass
class CompletedUserTask:
    id: int
    userId: int
    taskId: int
    completeTime: str
