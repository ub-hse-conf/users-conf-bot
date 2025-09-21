from typing import List

from src.api.client.base_client import BaseClient
from src.exception import ServerErrorException
from src.models import CreateUserRequest, CreateUserResponse, Error, VisitResult, User, ErrorType, UserTask, Vote, \
    CreateVoteRequest, Activity
from src.models.activity import ActivityRequest
from src.models.company import Company
from src.models.keyword import Keyword
from src.models.task import CompletedUserTask
from src.utils.mapper import user_from_json, visit_result_from_json, user_task_from_json, parse_error, \
    company_info_from_json, completed_task_from_json, vote_from_json, activities_from_json


class UserClient(BaseClient):
    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        url = "/users"

        payload = {
            "course": request.course,
            "fullName": request.fullName,
            "program": request.program,
            "email": request.email,
            "tgId": request.tgId
        }

        result = await self._post_request_or_error(url, payload)
        if isinstance(result, Error):
            raise ServerErrorException("Error while creating user", result)

        return CreateUserResponse(
            user=user_from_json(result)
        )

    async def get_user_data(self, tg_id: int) -> User | Error:
        url = f"/users/{tg_id}"
        result = await self._get_request_or_error(url)
        if isinstance(result, Error):
            raise ServerErrorException("Error while getting user data", result)

        return user_from_json(result)

    async def exists_user(self, tg_id: int) -> bool | Error:
        url = f"/users/{tg_id}"
        client: UserClient
        async with self as client:
            response = await client._get_request(url)
            if response.status_code == 404:
                return False

            elif response.status_code == 200:
                return True

            return parse_error(response.json())

    async def get_user_qr(self, tg_id: int) -> bytes:
        url = f"/users/{tg_id}/qr"

        async with self as client:
            result = await client._get_request(url)
            if result.is_error:
                error = self._parse_error(result.json())
                raise ServerErrorException("Error while getting user qr code", error)

            return result.content

    async def get_user_tasks(self, tg_id: int) -> List[UserTask]:
        url = f"/users/{tg_id}/tasks"

        result = await self._get_request_or_error(url)
        if isinstance(result, Error):
            raise ServerErrorException("Error while getting user tasks", result)

        return list(map(user_task_from_json, result))

    async def get_user_task_by_id(self, tg_id: int, task_id: int) -> UserTask:
        url = f"/users/{tg_id}/tasks/{task_id}"

        result = await self._get_request_or_error(url)
        if isinstance(result, Error):
            raise ServerErrorException(f"Error while getting user task with id {task_id}", result)

        return user_task_from_json(result)

    async def visit_company(self, tg_id: int, code: str) -> VisitResult | None:
        url = f"/users/{tg_id}/visits/{code}"
        result = await self._post_request_or_error(url)
        if isinstance(result, Error):
            if result.error_type == ErrorType.VISIT_ALREADY_EXISTS:
                return None
            raise ServerErrorException(f"Error while visiting company for code {code}", result)

        return visit_result_from_json(result)

    async def get_user_visits(self, tg_id: int) -> List[VisitResult]:
        url = f"/users/{tg_id}/visits"
        result = await self._get_request_or_error(url)

        if isinstance(result, Error):
            raise ServerErrorException("Error while getting user visits", result)

        return list(map(visit_result_from_json, result))

    async def get_company_info(self, company_id: int) -> Company | Error:
        url = f"/companies/{company_id}"
        result = await self._get_request_or_error(url)
        if isinstance(result, Error):
            raise ServerErrorException(f"Error while get information about company with id {company_id}", result)

        return company_info_from_json(result)

    async def complete_task(self, task_id: int, tg_id: int) -> CompletedUserTask | None:
        url = f"/tasks/{task_id}/submit/{tg_id}"
        result = await self._post_request_or_error(url)
        if isinstance(result, Error):
            if result.error_type == ErrorType.USER_NOT_FOUND:
                return None
            raise ServerErrorException(f"Error while completing task {task_id}", result)

        return completed_task_from_json(result)

    async def add_user_answer(self, activity_id: int, request: CreateVoteRequest) -> Vote | None:
        url = f"/activities/{activity_id}/event/answer"

        payload = {
            "userTgId": request.userTgId,
            "answer": request.answer,
        }

        result = await self._post_request_or_error(url, payload)

        if isinstance(result, Error):
            if result.error_type == ErrorType.USER_NOT_FOUND:
                return None
            raise ServerErrorException(f"Error while vote {activity_id}", result)

        return vote_from_json(result)

    async def add_keyword(self, keyword: Keyword) -> str | None:
        url = f"/activities/key-word"

        payload = {
            "tgId": keyword.tgId,
            "keyWord": keyword.keyWord,
        }

        result = await self._post_request_or_error(url, payload)

        if isinstance(result, Error):
            if result.error_type == ErrorType.ACTIVITY_NOT_FOUND:
                return "Unavailable activity"
            raise ServerErrorException(f"Error while sending keyword", result)

    async def get_all_activities(self) -> List[ActivityRequest] | Error:
        url = f"/activities/"

        result = await self._get_request_or_error(url)

        if isinstance(result, Error):
            raise ServerErrorException(f"Error while get information about all activities", result)

        return list(map(activities_from_json, result))
