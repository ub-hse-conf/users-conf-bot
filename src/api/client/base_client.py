import uuid
from typing import Any, Optional, Dict

import httpx
from structlog.contextvars import get_contextvars

from src.models import Error, ErrorType


class BaseClient:
    def __init__(self, base_url: str, username: str, password: str):
        self._base_url = base_url
        self._headers = {
            'Content-Type': 'application/json',
        }
        self.username = username
        self.password = password
        self._client: Optional[httpx.AsyncClient] = None
        self._timeout = httpx.Timeout(60.0)

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=self._timeout,
            auth=(self.username, self.password),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def _get_request_or_error(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> dict | Error:
        async with self as client:
            response = await client._get_request(uri, payload)
            if response.is_error:
                return self._parse_error(response.json())

            return response.json()

    async def _get_request(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._make_request("GET", uri, payload)

    async def _post_request_or_error(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> dict | Error:
        async with self as client:
            response = await client._post_request(uri, payload)
            if response.is_error:
                return self._parse_error(response.json())

            return response.json()

    async def _post_request(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._make_request("POST", uri, payload)

    async def _delete_request(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._make_request("DELETE", uri, payload)

    async def _patch_request_or_error(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> dict | Error:
        async with self as client:
            response = await client._patch_request(uri, payload)
            if response.is_error:
                return self._parse_error(response.json())

            return response.json()

    async def _patch_request(
            self,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._make_request("PATCH", uri, payload)

    async def _make_request(
            self,
            method: str,
            uri: str,
            payload: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        if not self._client:
            raise RuntimeError("Client not initialized. Use async with.")

        headers = {
            **self._headers,
            "X-Request-Id": str(self._get_trace_id())
        }

        if not uri.startswith("/"):
            uri = "/" + uri

        return await self._client.request(
            method=method,
            url=uri,
            json=payload,
            headers=headers,
        )

    def _get_trace_headers(self) -> Dict[str, Any]:
        return {
            "X-Request-Id": str(self._get_trace_id())
        }

    def _get_trace_id(self) -> str:
        context = get_contextvars()
        return context.get("request_id", str(uuid.uuid4()))

    def _parse_error(self, error: dict) -> Error:
        return Error(
            error_type=ErrorType[error["errorType"]],
            message=error["message"],
        )