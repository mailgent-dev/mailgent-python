import httpx
import pytest
import respx
from mailgent._http import SyncHttpClient, AsyncHttpClient
from mailgent._errors import MailgentError


class TestSyncHttpClient:
    @respx.mock
    def test_get_success(self):
        respx.get("https://api.mailgent.dev/v0/whoami").mock(
            return_value=httpx.Response(200, json={"identityId": "id-123"}))
        client = SyncHttpClient("https://api.mailgent.dev", "mgent-test")
        result = client.get("/v0/whoami")
        assert result["identityId"] == "id-123"
        client.close()

    @respx.mock
    def test_auth_header(self):
        route = respx.get("https://api.mailgent.dev/v0/whoami").mock(
            return_value=httpx.Response(200, json={}))
        client = SyncHttpClient("https://api.mailgent.dev", "mgent-secret")
        client.get("/v0/whoami")
        assert route.calls[0].request.headers["authorization"] == "Bearer mgent-secret"
        client.close()

    @respx.mock
    def test_post_with_body(self):
        respx.post("https://api.mailgent.dev/v0/messages/send").mock(
            return_value=httpx.Response(201, json={"messageId": "msg-1"}))
        client = SyncHttpClient("https://api.mailgent.dev", "mgent-test")
        result = client.post("/v0/messages/send", json={"to": ["a@b.com"], "subject": "Hi", "text": "Hello"})
        assert result["messageId"] == "msg-1"
        client.close()

    @respx.mock
    def test_delete_204(self):
        respx.delete("https://api.mailgent.dev/v0/messages/msg-1").mock(
            return_value=httpx.Response(204))
        client = SyncHttpClient("https://api.mailgent.dev", "mgent-test")
        assert client.delete("/v0/messages/msg-1") is None
        client.close()

    @respx.mock
    def test_error_raises(self):
        respx.get("https://api.mailgent.dev/v0/whoami").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized", "message": "Invalid API key"}))
        client = SyncHttpClient("https://api.mailgent.dev", "mgent-bad")
        with pytest.raises(MailgentError) as exc_info:
            client.get("/v0/whoami")
        assert exc_info.value.status == 401
        client.close()


class TestAsyncHttpClient:
    @respx.mock
    @pytest.mark.asyncio
    async def test_get_success(self):
        respx.get("https://api.mailgent.dev/v0/whoami").mock(
            return_value=httpx.Response(200, json={"identityId": "id-123"}))
        client = AsyncHttpClient("https://api.mailgent.dev", "mgent-test")
        result = await client.get("/v0/whoami")
        assert result["identityId"] == "id-123"
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_error_raises(self):
        respx.get("https://api.mailgent.dev/v0/whoami").mock(
            return_value=httpx.Response(403, json={"error": "forbidden", "message": "No access"}))
        client = AsyncHttpClient("https://api.mailgent.dev", "mgent-test")
        with pytest.raises(MailgentError) as exc_info:
            await client.get("/v0/whoami")
        assert exc_info.value.status == 403
        await client.close()
