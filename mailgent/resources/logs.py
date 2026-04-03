from __future__ import annotations
from typing import Any, Optional
from mailgent.types import ActivityLog, LogsStats


class LogsResource:
    def __init__(self, http):
        self._http = http

    def list(self, limit: Optional[int] = None, category: Optional[str] = None,
             action: Optional[str] = None, status: Optional[str] = None,
             severity: Optional[str] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if category: params["category"] = category
        if action: params["action"] = action
        if status: params["status"] = status
        if severity: params["severity"] = severity
        if page_token: params["pageToken"] = page_token
        data = self._http.get("/v0/logs", params=params or None)
        return {"logs": [ActivityLog.from_dict(l) for l in data.get("logs", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    def stats(self) -> LogsStats:
        return LogsStats.from_dict(self._http.get("/v0/logs/stats"))


class AsyncLogsResource:
    def __init__(self, http):
        self._http = http

    async def list(self, limit: Optional[int] = None, category: Optional[str] = None,
                   action: Optional[str] = None, status: Optional[str] = None,
                   severity: Optional[str] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if category: params["category"] = category
        if action: params["action"] = action
        if status: params["status"] = status
        if severity: params["severity"] = severity
        if page_token: params["pageToken"] = page_token
        data = await self._http.get("/v0/logs", params=params or None)
        return {"logs": [ActivityLog.from_dict(l) for l in data.get("logs", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    async def stats(self) -> LogsStats:
        return LogsStats.from_dict(await self._http.get("/v0/logs/stats"))
