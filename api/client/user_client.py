from typing import List

from api.client.base_client import BaseClient
from models import CreateUserRequest, CreateUserResponse, Error, VisitResult
from models.task import Task


class UserClient(BaseClient):
    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse | Error:
        url = "/users"

        payload = {
            "course": request.course,
            "fullName": request.fullName,
            "program": request.program,
            "email": request.email,
            "tgId": request.tgId
        }

        return await self._post_request_or_error(url, payload)

    async def get_user_data(self, tg_id: int) -> dict | Error:
        url = f"/users/{tg_id}"
        return await self._get_request_or_error(url)

    async def get_user_qr(self, tg_id: int) -> bytes | Error:
        url = f"/users/{tg_id}/qr"
        return await self._get_request_or_error(url)

    async def get_user_tasks(self, tg_id: int) -> Task | Error:
        url = f"/users/{tg_id}/tasks"
        return await self._get_request_or_error(url)

    async def get_user_task_by_id(self, tg_id: int, task_id: int) -> List[Task] | Error:
        url = f"/users/{tg_id}/tasks/{task_id}"
        return await self._get_request_or_error(url)

    async def visit_activity(self, tg_id: int, code: str) -> VisitResult | Error:
        url = f"/users/{tg_id}/visits/{code}"
        return await self._post_request_or_error(url)

    async def get_user_activities(self, tg_id: int) -> List[VisitResult] | Error:
        url = f"/users/{tg_id}/visits"
        return await self._get_request_or_error(url)
