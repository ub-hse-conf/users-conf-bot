from typing import List

from src.api.client.base_client import BaseClient
from src.exception import ServerErrorException
from src.models import CreateUserRequest, CreateUserResponse, Error, VisitResult, User, ErrorType, UserTask
from src.utils.mapper import user_from_json, visit_result_from_json, user_task_from_json


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

    async def get_user_data(self, tg_id: int) -> User:
        url = f"/users/{tg_id}"
        result = await self._get_request_or_error(url)
        if isinstance(result, Error):
            raise ServerErrorException("Error while getting user data", result)

        return user_from_json(result)

    async def get_user_qr(self, tg_id: int) -> bytes:
        url = f"/users/{tg_id}/qr"

        result = await self._get_request(url)
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
