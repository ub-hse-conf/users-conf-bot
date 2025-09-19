from dataclasses import dataclass

from src.models.activity.activity_type import ActivityType


@dataclass
class Activity:
    id: int
    name: str
    description: str
    activityType: ActivityType
    location: str
    startTime: str
    endTime: str
    points: int
