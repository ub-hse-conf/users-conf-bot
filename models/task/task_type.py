from enum import Enum


class TaskType(str, Enum):
    PERMANENT = "PERMANENT"
    TEMP = "TEMP"
