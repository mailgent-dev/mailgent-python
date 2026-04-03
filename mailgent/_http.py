from __future__ import annotations

from typing import Any, Optional

import httpx

from mailgent._errors import MailgentError

DEFAULT_BASE_URL = "https://api.mailgent.dev"
DEFAULT_TIMEOUT = 30.0


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _handle_response(response: httpx.Response) -> Any:
    if response.status_code == 204:
        return None

    data = response.json() if response.content else {}

    if not response.is_success:
        raise MailgentError(
            status=response.status_code,
            code=data.get("error", "unknown_error"),
            message=data.get("message", f"Request failed with status {response.status_code}"),
        )

    return data


class SyncHttpClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=_build_headers(api_key),
            timeout=timeout,
        )

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(self._client.get(path, params=params))

    def post(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(self._client.post(path, json=json))

    def put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(self._client.put(path, json=json))

    def patch(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(self._client.patch(path, json=json))

    def delete(self, path: str) -> Any:
        return _handle_response(self._client.delete(path))

    def close(self) -> None:
        self._client.close()


class AsyncHttpClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers=_build_headers(api_key),
            timeout=timeout,
        )

    async def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(await self._client.get(path, params=params))

    async def post(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(await self._client.post(path, json=json))

    async def put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(await self._client.put(path, json=json))

    async def patch(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return _handle_response(await self._client.patch(path, json=json))

    async def delete(self, path: str) -> Any:
        return _handle_response(await self._client.delete(path))

    async def close(self) -> None:
        await self._client.aclose()
