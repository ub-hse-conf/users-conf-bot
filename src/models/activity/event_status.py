from enum import Enum


class EventStatus(str, Enum):
    PREPARED = "PREPARED"
    CONTINUED = "CONTINUED"
    ENDED = "ENDED"
