from dataclasses import dataclass

from src.models.activity import Activity
from src.models.activity.visitable import Visitable
from src.models.activity.target_type import TargetType


@dataclass
class VisitResult:
    target: Visitable
    type: TargetType
