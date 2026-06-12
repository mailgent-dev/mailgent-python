import httpx
import pytest
import respx
from mailgent import Mailgent, AsyncMailgent
from mailgent.types import (
    SlackChannel,
    SlackConnectResponse,
    SlackConnection,
    SlackMessage,
    SlackSendMessageResponse,
)


class TestSlackResource:
    @respx.mock
    def test_connection_connected(self):
        respx.get("https://api.mailgent.dev/v0/slack/connection").mock(
            return_value=httpx.Response(200, json={
                "connected": True, "teamId": "T123", "teamName": "Acme",
                "botUserId": "U456", "slackScopes": "chat:write,channels:read",
                "installedAt": "2026-06-01T00:00:00Z",
            }))
        client = Mailgent(api_key="loid-test")
        result = client.slack.connection()
        assert isinstance(result, SlackConnection)
        assert result.connected is True
        assert result.team_id == "T123"
        assert result.team_name == "Acme"
        assert result.bot_user_id == "U456"
        assert result.installed_at == "2026-06-01T00:00:00Z"
        client.close()

    @respx.mock
    def test_connection_not_connected(self):
        respx.get("https://api.mailgent.dev/v0/slack/connection").mock(
            return_value=httpx.Response(200, json={"connected": False}))
        client = Mailgent(api_key="loid-test")
        result = client.slack.connection()
        assert result.connected is False
        assert result.team_id is None
        client.close()

    @respx.mock
    def test_connect(self):
        respx.post("https://api.mailgent.dev/v0/slack/connect").mock(
            return_value=httpx.Response(200, json={
                "installUrl": "https://slack.com/oauth/v2/authorize?state=abc",
                "expiresInSeconds": 600,
                "message": "Open the install URL in a browser",
            }))
        client = Mailgent(api_key="loid-test")
        result = client.slack.connect()
        assert isinstance(result, SlackConnectResponse)
        assert result.install_url.startswith("https://slack.com/oauth")
        assert result.expires_in_seconds == 600
        client.close()

    @respx.mock
    def test_disconnect(self):
        respx.delete("https://api.mailgent.dev/v0/slack/connection").mock(
            return_value=httpx.Response(200, json={"message": "Slack disconnected"}))
        client = Mailgent(api_key="loid-test")
        result = client.slack.disconnect()
        assert result["message"] == "Slack disconnected"
        client.close()

    @respx.mock
    def test_list_channels(self):
        respx.get("https://api.mailgent.dev/v0/slack/channels").mock(
            return_value=httpx.Response(200, json={
                "channels": [
                    {"id": "C1", "name": "general", "isPrivate": False, "botIsMember": True},
                    {"id": "C2", "name": "secret", "isPrivate": True, "botIsMember": False},
                ],
            }))
        client = Mailgent(api_key="loid-test")
        result = client.slack.list_channels()
        assert len(result["channels"]) == 2
        assert isinstance(result["channels"][0], SlackChannel)
        assert result["channels"][0].name == "general"
        assert result["channels"][1].is_private is True
        assert result["channels"][1].bot_is_member is False
        client.close()

    @respx.mock
    def test_send_message(self):
        route = respx.post("https://api.mailgent.dev/v0/slack/messages").mock(
            return_value=httpx.Response(201, json={"channel": "C1", "ts": "1718000000.000100"}))
        client = Mailgent(api_key="loid-test")
        result = client.slack.send_message("#general", "Deploy finished")
        assert isinstance(result, SlackSendMessageResponse)
        assert result.channel == "C1"
        assert result.ts == "1718000000.000100"
        import json
        body = json.loads(route.calls.last.request.content)
        assert body == {"channel": "#general", "text": "Deploy finished"}
        client.close()

    @respx.mock
    def test_send_message_in_thread(self):
        route = respx.post("https://api.mailgent.dev/v0/slack/messages").mock(
            return_value=httpx.Response(201, json={"channel": "C1", "ts": "1718000000.000200"}))
        client = Mailgent(api_key="loid-test")
        client.slack.send_message("C1", "Reply", thread_ts="1718000000.000100")
        import json
        body = json.loads(route.calls.last.request.content)
        assert body["threadTs"] == "1718000000.000100"
        client.close()

    @respx.mock
    def test_list_messages(self):
        respx.get("https://api.mailgent.dev/v0/slack/messages").mock(
            return_value=httpx.Response(200, json={
                "messages": [{
                    "id": "msg-1", "channelId": "C1", "userId": "U9",
                    "text": "hello bot", "ts": "1718000000.000100", "threadTs": None,
                    "eventType": "message", "receivedAt": "2026-06-10T00:00:00Z",
                }],
            }))
        client = Mailgent(api_key="loid-test")
        result = client.slack.list_messages(channel="C1", limit=10)
        assert len(result["messages"]) == 1
        msg = result["messages"][0]
        assert isinstance(msg, SlackMessage)
        assert msg.channel_id == "C1"
        assert msg.text == "hello bot"
        assert msg.thread_ts is None
        client.close()

    def test_client_has_slack(self):
        client = Mailgent(api_key="loid-test")
        assert client.slack is not None
        client.close()


class TestAsyncSlackResource:
    def test_async_client_has_slack(self):
        client = AsyncMailgent(api_key="loid-test")
        assert client.slack is not None

    @respx.mock
    @pytest.mark.asyncio
    async def test_send_message_async(self):
        respx.post("https://api.mailgent.dev/v0/slack/messages").mock(
            return_value=httpx.Response(201, json={"channel": "C1", "ts": "1718000000.000100"}))
        client = AsyncMailgent(api_key="loid-test")
        result = await client.slack.send_message("#general", "hi")
        assert result.ts == "1718000000.000100"
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_channels_async(self):
        respx.get("https://api.mailgent.dev/v0/slack/channels").mock(
            return_value=httpx.Response(200, json={
                "channels": [{"id": "C1", "name": "general", "isPrivate": False, "botIsMember": True}],
            }))
        client = AsyncMailgent(api_key="loid-test")
        result = await client.slack.list_channels()
        assert result["channels"][0].id == "C1"
        await client.close()
