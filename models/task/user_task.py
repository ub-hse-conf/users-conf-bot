from dataclasses import dataclass


@dataclass
class UserTask:
    id: int
    name: str
    description: str
    isAvailable: bool
    status: str
    taskType: str
