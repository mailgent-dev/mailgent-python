from __future__ import annotations
from typing import Any, Optional
from hivekey.types import CalendarEvent


class CalendarResource:
    def __init__(self, http):
        self._http = http

    def create(self, title: str, start_at: str, end_at: Optional[str] = None,
               is_all_day: bool = False, description: Optional[str] = None,
               location: Optional[str] = None, metadata: Optional[dict[str, Any]] = None) -> CalendarEvent:
        body: dict[str, Any] = {"title": title, "startAt": start_at, "isAllDay": is_all_day}
        if end_at: body["endAt"] = end_at
        if description: body["description"] = description
        if location: body["location"] = location
        if metadata: body["metadata"] = metadata
        return CalendarEvent.from_dict(self._http.post("/v0/calendar", json=body))

    def list(self, limit: Optional[int] = None, from_date: Optional[str] = None,
             to_date: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if from_date: params["from"] = from_date
        if to_date: params["to"] = to_date
        data = self._http.get("/v0/calendar", params=params or None)
        return {"events": [CalendarEvent.from_dict(e) for e in data.get("events", [])], "count": data["count"]}

    def get(self, event_id: str) -> CalendarEvent:
        return CalendarEvent.from_dict(self._http.get(f"/v0/calendar/{event_id}"))

    def update(self, event_id: str, title: Optional[str] = None, start_at: Optional[str] = None,
               end_at: Optional[str] = None, is_all_day: Optional[bool] = None,
               description: Optional[str] = None, location: Optional[str] = None) -> CalendarEvent:
        body: dict[str, Any] = {}
        if title is not None: body["title"] = title
        if start_at is not None: body["startAt"] = start_at
        if end_at is not None: body["endAt"] = end_at
        if is_all_day is not None: body["isAllDay"] = is_all_day
        if description is not None: body["description"] = description
        if location is not None: body["location"] = location
        return CalendarEvent.from_dict(self._http.patch(f"/v0/calendar/{event_id}", json=body))

    def delete(self, event_id: str) -> None:
        self._http.delete(f"/v0/calendar/{event_id}")

    def set_public(self, enabled: bool) -> dict[str, bool]:
        return self._http.post("/v0/calendar/public", json={"enabled": enabled})


class AsyncCalendarResource:
    def __init__(self, http):
        self._http = http

    async def create(self, title: str, start_at: str, end_at: Optional[str] = None,
                     is_all_day: bool = False, description: Optional[str] = None,
                     location: Optional[str] = None, metadata: Optional[dict[str, Any]] = None) -> CalendarEvent:
        body: dict[str, Any] = {"title": title, "startAt": start_at, "isAllDay": is_all_day}
        if end_at: body["endAt"] = end_at
        if description: body["description"] = description
        if location: body["location"] = location
        if metadata: body["metadata"] = metadata
        return CalendarEvent.from_dict(await self._http.post("/v0/calendar", json=body))

    async def list(self, limit: Optional[int] = None, from_date: Optional[str] = None,
                   to_date: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if from_date: params["from"] = from_date
        if to_date: params["to"] = to_date
        data = await self._http.get("/v0/calendar", params=params or None)
        return {"events": [CalendarEvent.from_dict(e) for e in data.get("events", [])], "count": data["count"]}

    async def get(self, event_id: str) -> CalendarEvent:
        return CalendarEvent.from_dict(await self._http.get(f"/v0/calendar/{event_id}"))

    async def update(self, event_id: str, title: Optional[str] = None, start_at: Optional[str] = None,
                     end_at: Optional[str] = None, is_all_day: Optional[bool] = None,
                     description: Optional[str] = None, location: Optional[str] = None) -> CalendarEvent:
        body: dict[str, Any] = {}
        if title is not None: body["title"] = title
        if start_at is not None: body["startAt"] = start_at
        if end_at is not None: body["endAt"] = end_at
        if is_all_day is not None: body["isAllDay"] = is_all_day
        if description is not None: body["description"] = description
        if location is not None: body["location"] = location
        return CalendarEvent.from_dict(await self._http.patch(f"/v0/calendar/{event_id}", json=body))

    async def delete(self, event_id: str) -> None:
        await self._http.delete(f"/v0/calendar/{event_id}")

    async def set_public(self, enabled: bool) -> dict[str, bool]:
        return await self._http.post("/v0/calendar/public", json={"enabled": enabled})
