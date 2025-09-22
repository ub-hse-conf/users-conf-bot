from enum import Enum


class TaskStatus(str, Enum):
    READY = "READY"
    IN_PROCESS = "IN_PROCESS"
    FINISHED = "FINISHED"
