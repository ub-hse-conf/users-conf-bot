from enum import Enum


class ActivityType(str, Enum):
    LECTURE = "LECTURE"
    CONTEST = "CONTEST"
    WORKSHOP = "WORKSHOP"
