from dataclasses import dataclass

from src.models.task.task_status import TaskStatus
from src.models.task.task_type import TaskType


@dataclass
class Task:
    id: int
    type: TaskType
    description: str
    duration: str
    name: str
    status: TaskStatus
    points: int
