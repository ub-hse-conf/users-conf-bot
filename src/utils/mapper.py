from src.models import User, VisitResult, Visitable, TargetType, UserTask, UserTaskStatus
from src.models.task import UserTaskType


def user_from_json(json: dict) -> User:
    return User(
        userId=int(json["userId"]),
        name=json["name"],
        email=json["email"],
        course=int(json["course"]),
        program=json["program"]
    )

def visit_result_from_json(json: dict) -> VisitResult:
    return VisitResult(
        target=Visitable(
            id=int(json["target"]["id"]),
            name=json["target"]["name"],
            description=json["target"]["description"],
        ),
        targetType=TargetType["targetType"],
    )

def user_task_from_json(json: dict) -> UserTask:
    return UserTask(
        id=int(json["id"]),
        name=json["name"],
        description=json["description"],
        is_available=json["isAvailable"],
        status=UserTaskStatus[json["status"]],
        task_type=UserTaskType[json["taskType"]],
    )