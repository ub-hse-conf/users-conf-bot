from enum import Enum


class UserTaskStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
