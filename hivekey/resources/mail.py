from __future__ import annotations
from typing import Any, Optional
from hivekey.types import MessageResponse, ThreadResponse, ThreadDetailResponse


class MailResource:
    def __init__(self, http):
        self._http = http

    def send(self, to: list[str], subject: str, text: str, html: Optional[str] = None,
             cc: Optional[list[str]] = None, bcc: Optional[list[str]] = None) -> MessageResponse:
        body: dict[str, Any] = {"to": to, "subject": subject, "text": text}
        if html: body["html"] = html
        if cc: body["cc"] = cc
        if bcc: body["bcc"] = bcc
        return MessageResponse.from_dict(self._http.post("/v0/messages/send", json=body))

    def reply(self, message_id: str, text: str, html: Optional[str] = None) -> MessageResponse:
        body: dict[str, Any] = {"text": text}
        if html: body["html"] = html
        return MessageResponse.from_dict(self._http.post(f"/v0/messages/{message_id}/reply", json=body))

    def list_messages(self, limit: Optional[int] = None, labels: Optional[str] = None,
                      page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if labels: params["labels"] = labels
        if page_token: params["pageToken"] = page_token
        data = self._http.get("/v0/messages", params=params or None)
        return {"messages": [MessageResponse.from_dict(m) for m in data.get("messages", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    def get_message(self, message_id: str) -> MessageResponse:
        return MessageResponse.from_dict(self._http.get(f"/v0/messages/{message_id}"))

    def update_labels(self, message_id: str, add_labels: Optional[list[str]] = None,
                      remove_labels: Optional[list[str]] = None) -> MessageResponse:
        body: dict[str, Any] = {}
        if add_labels: body["addLabels"] = add_labels
        if remove_labels: body["removeLabels"] = remove_labels
        return MessageResponse.from_dict(self._http.patch(f"/v0/messages/{message_id}", json=body))

    def delete_message(self, message_id: str) -> None:
        self._http.delete(f"/v0/messages/{message_id}")

    def list_threads(self, limit: Optional[int] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if page_token: params["pageToken"] = page_token
        data = self._http.get("/v0/threads", params=params or None)
        return {"threads": [ThreadResponse.from_dict(t) for t in data.get("threads", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    def get_thread(self, thread_id: str, limit: Optional[int] = None) -> ThreadDetailResponse:
        params = {"limit": limit} if limit else None
        return ThreadDetailResponse.from_dict(self._http.get(f"/v0/threads/{thread_id}", params=params))

    def delete_thread(self, thread_id: str) -> None:
        self._http.delete(f"/v0/threads/{thread_id}")


class AsyncMailResource:
    def __init__(self, http):
        self._http = http

    async def send(self, to: list[str], subject: str, text: str, html: Optional[str] = None,
                   cc: Optional[list[str]] = None, bcc: Optional[list[str]] = None) -> MessageResponse:
        body: dict[str, Any] = {"to": to, "subject": subject, "text": text}
        if html: body["html"] = html
        if cc: body["cc"] = cc
        if bcc: body["bcc"] = bcc
        return MessageResponse.from_dict(await self._http.post("/v0/messages/send", json=body))

    async def reply(self, message_id: str, text: str, html: Optional[str] = None) -> MessageResponse:
        body: dict[str, Any] = {"text": text}
        if html: body["html"] = html
        return MessageResponse.from_dict(await self._http.post(f"/v0/messages/{message_id}/reply", json=body))

    async def list_messages(self, limit: Optional[int] = None, labels: Optional[str] = None,
                            page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if labels: params["labels"] = labels
        if page_token: params["pageToken"] = page_token
        data = await self._http.get("/v0/messages", params=params or None)
        return {"messages": [MessageResponse.from_dict(m) for m in data.get("messages", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    async def get_message(self, message_id: str) -> MessageResponse:
        return MessageResponse.from_dict(await self._http.get(f"/v0/messages/{message_id}"))

    async def update_labels(self, message_id: str, add_labels: Optional[list[str]] = None,
                            remove_labels: Optional[list[str]] = None) -> MessageResponse:
        body: dict[str, Any] = {}
        if add_labels: body["addLabels"] = add_labels
        if remove_labels: body["removeLabels"] = remove_labels
        return MessageResponse.from_dict(await self._http.patch(f"/v0/messages/{message_id}", json=body))

    async def delete_message(self, message_id: str) -> None:
        await self._http.delete(f"/v0/messages/{message_id}")

    async def list_threads(self, limit: Optional[int] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if page_token: params["pageToken"] = page_token
        data = await self._http.get("/v0/threads", params=params or None)
        return {"threads": [ThreadResponse.from_dict(t) for t in data.get("threads", [])],
                "count": data["count"], "next_page_token": data.get("nextPageToken")}

    async def get_thread(self, thread_id: str, limit: Optional[int] = None) -> ThreadDetailResponse:
        params = {"limit": limit} if limit else None
        return ThreadDetailResponse.from_dict(await self._http.get(f"/v0/threads/{thread_id}", params=params))

    async def delete_thread(self, thread_id: str) -> None:
        await self._http.delete(f"/v0/threads/{thread_id}")
