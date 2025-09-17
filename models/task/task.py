from dataclasses import dataclass
from typing import Optional

from anyio.abc import TaskStatus

from models.task.task_type import TaskType


@dataclass
class Task:
    id: int
    type: TaskType
    name: str
    status: TaskStatus
    description: str
    points: int
    duration: Optional[str] = None
