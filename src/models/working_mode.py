import enum


class WorkingMode(enum.Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"