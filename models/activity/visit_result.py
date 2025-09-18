from dataclasses import dataclass

from models.activity.activity import Activity
from models.activity.target_type import TargetType


@dataclass
class VisitResult:
    target: Activity
    targetType: TargetType
