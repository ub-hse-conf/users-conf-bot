from src.models import User, VisitResult, Visitable, TargetType, UserTask, UserTaskStatus, Error, ErrorType, Activity, \
    Vote
from src.models.company import Company
from src.models.task import UserTaskType, CompletedUserTask


def user_from_json(json: dict) -> User:
    return User(
        userId=int(json["userId"]),
        fullName=json["fullName"],
        email=json["email"],
        course=int(json["course"]),
        program=json["program"],
        role=json["role"]
    )


def visit_result_from_json(json: dict) -> VisitResult:
    return VisitResult(
        target=Visitable(
            id=int(json["target"]["id"]),
            name=json["target"]["name"],
            description=json["target"]["description"],
        ),
        targetType=TargetType[json["targetType"]],
    )


def company_info_from_json(json: dict) -> Company:
    return Company(
        name=json["name"],
        description=json["description"],
        siteUrl=json["siteUrl"],
        id=int(json["id"])
    )


def completed_task_from_json(json: dict) -> CompletedUserTask:
    return CompletedUserTask(
        id=int(json["id"]),
        userId=int(json["userId"]),
        taskId=int(json["taskId"]),
        completeTime=json["completeTime"]
    )


# def visit_result_from_json(json: dict) -> VisitResult:
#     return VisitResult(
#         target=Activity(
#             id=int(json["target"]["id"]),
#             name=json["target"]["name"],
#             description=json["target"]["description"],
#             activityType=json["target"]["activityType"],
#             endTime=json["target"]["endTime"],
#             startTime=json["target"]["startTime"],
#             location=json["target"]["location"],
#             points=json["target"]["points"]
#
#         ),
#         targetType=TargetType[json["type"]],
#     )


def user_task_from_json(json: dict) -> UserTask:
    return UserTask(
        id=int(json["id"]),
        name=json["name"],
        description=json["description"],
        is_available=json["isAvailable"],
        status=UserTaskStatus[json["status"]],
        task_type=UserTaskType[json["taskType"]],
    )


def parse_error(json: dict) -> Error:
    return Error(
        error_type=ErrorType[json["errorType"]],
        message=json["message"],
    )


def vote_from_json(json: dict) -> Vote:
    return Vote(
        id=int(json["voteId"]),
        userId=int(json["userId"]),
        answer=json["answer"],
        eventId=json["eventId"]
    )
