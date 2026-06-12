from __future__ import annotations
from typing import Any, Optional
from mailgent.types import (
    SlackChannel,
    SlackConnectResponse,
    SlackConnection,
    SlackMessage,
    SlackSendMessageResponse,
)


class SlackResource:
    """Synchronous ``mailgent.slack`` resource.

    Bridges your agent into a Slack workspace. Run ``connect()`` once to get
    an OAuth install link, open it in a browser, then send and read messages.
    Reading requires the ``slack:read`` scope; sending requires ``slack:send``.
    """

    def __init__(self, http):
        self._http = http

    def connection(self) -> SlackConnection:
        """Get the current Slack workspace connection status."""
        return SlackConnection.from_dict(self._http.get("/v0/slack/connection"))

    def connect(self) -> SlackConnectResponse:
        """Generate a short-lived OAuth install link. Open ``install_url``
        in a browser to connect a Slack workspace."""
        return SlackConnectResponse.from_dict(self._http.post("/v0/slack/connect"))

    def disconnect(self) -> dict[str, Any]:
        """Disconnect the Slack workspace."""
        return self._http.delete("/v0/slack/connection")

    def list_channels(self) -> dict[str, Any]:
        """List channels visible to the bot. ``bot_is_member`` tells you
        whether the bot can post without being invited first."""
        data = self._http.get("/v0/slack/channels")
        return {"channels": [SlackChannel.from_dict(c) for c in data.get("channels", [])]}

    def send_message(self, channel: str, text: str,
                     thread_ts: Optional[str] = None) -> SlackSendMessageResponse:
        """Send a message to a channel (id or name). Pass ``thread_ts`` to
        reply in a thread."""
        body: dict[str, Any] = {"channel": channel, "text": text}
        if thread_ts: body["threadTs"] = thread_ts
        return SlackSendMessageResponse.from_dict(self._http.post("/v0/slack/messages", json=body))

    def list_messages(self, channel: Optional[str] = None, since: Optional[str] = None,
                      limit: Optional[int] = None) -> dict[str, Any]:
        """List messages received by the bot, newest first."""
        params: dict[str, Any] = {}
        if channel: params["channel"] = channel
        if since: params["since"] = since
        if limit is not None: params["limit"] = limit
        data = self._http.get("/v0/slack/messages", params=params or None)
        return {"messages": [SlackMessage.from_dict(m) for m in data.get("messages", [])]}


class AsyncSlackResource:
    """Asynchronous ``mailgent.slack`` resource. Same surface as
    :class:`SlackResource` with ``await`` on each method."""

    def __init__(self, http):
        self._http = http

    async def connection(self) -> SlackConnection:
        return SlackConnection.from_dict(await self._http.get("/v0/slack/connection"))

    async def connect(self) -> SlackConnectResponse:
        return SlackConnectResponse.from_dict(await self._http.post("/v0/slack/connect"))

    async def disconnect(self) -> dict[str, Any]:
        return await self._http.delete("/v0/slack/connection")

    async def list_channels(self) -> dict[str, Any]:
        data = await self._http.get("/v0/slack/channels")
        return {"channels": [SlackChannel.from_dict(c) for c in data.get("channels", [])]}

    async def send_message(self, channel: str, text: str,
                           thread_ts: Optional[str] = None) -> SlackSendMessageResponse:
        body: dict[str, Any] = {"channel": channel, "text": text}
        if thread_ts: body["threadTs"] = thread_ts
        return SlackSendMessageResponse.from_dict(await self._http.post("/v0/slack/messages", json=body))

    async def list_messages(self, channel: Optional[str] = None, since: Optional[str] = None,
                            limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if channel: params["channel"] = channel
        if since: params["since"] = since
        if limit is not None: params["limit"] = limit
        data = await self._http.get("/v0/slack/messages", params=params or None)
        return {"messages": [SlackMessage.from_dict(m) for m in data.get("messages", [])]}
