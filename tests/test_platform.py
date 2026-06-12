import os
import httpx
import pytest
import respx
from mailgent import MailgentPlatform, AsyncMailgentPlatform
from mailgent.types import CreateIdentityResponse, IdentityDetail, IdentitySummary, RotateKeyResponse


class TestMailgentPlatformClient:
    def test_requires_api_key(self):
        os.environ.pop("MAILGENT_PLATFORM_KEY", None)
        with pytest.raises(ValueError, match="Platform key is required"):
            MailgentPlatform()

    def test_creates_with_api_key(self):
        client = MailgentPlatform(api_key="mgpk-test123")
        assert client.identities is not None
        client.close()

    def test_reads_env_var(self):
        os.environ["MAILGENT_PLATFORM_KEY"] = "mgpk-fromenv"
        try:
            client = MailgentPlatform()
            assert client.identities is not None
            client.close()
        finally:
            del os.environ["MAILGENT_PLATFORM_KEY"]

    def test_context_manager(self):
        with MailgentPlatform(api_key="mgpk-test") as client:
            assert client.identities is not None


class TestAsyncMailgentPlatformClient:
    def test_requires_api_key(self):
        os.environ.pop("MAILGENT_PLATFORM_KEY", None)
        with pytest.raises(ValueError, match="Platform key is required"):
            AsyncMailgentPlatform()


class TestPlatformIdentitiesResource:
    @respx.mock
    def test_create(self):
        respx.post("https://api.mailgent.dev/v0/platform/identities").mock(
            return_value=httpx.Response(201, json={
                "identityId": "id-123", "name": "Agent", "type": "INBOX", "purpose": "BUYER",
                "emailAddress": "agent@mailgent.dev", "scopes": ["mail:read"],
                "apiKeyPrefix": "loid-abc1", "rawKey": "loid-abc123",
                "createdAt": "2026-01-01T00:00:00Z",
            }))
        client = MailgentPlatform(api_key="mgpk-test")
        result = client.identities.create(name="Agent", email_name="agent", scopes=["mail:read"])
        assert isinstance(result, CreateIdentityResponse)
        assert result.identity_id == "id-123"
        assert result.raw_key.startswith("loid-")
        client.close()

    @respx.mock
    def test_list(self):
        respx.get("https://api.mailgent.dev/v0/platform/identities").mock(
            return_value=httpx.Response(200, json={
                "identities": [{"identityId": "id-1", "name": "Agent", "type": "INBOX", "purpose": "BUYER",
                                "email": "a@b.dev", "scopes": ["mail:read"],
                                "usageCount": 5, "lastUsedAt": None, "createdAt": "2026-01-01T00:00:00Z"}],
                "count": 1,
            }))
        client = MailgentPlatform(api_key="mgpk-test")
        result = client.identities.list()
        assert result["count"] == 1
        assert len(result["identities"]) == 1
        assert isinstance(result["identities"][0], IdentitySummary)
        client.close()

    @respx.mock
    def test_get(self):
        respx.get("https://api.mailgent.dev/v0/platform/identities/id-123").mock(
            return_value=httpx.Response(200, json={
                "identityId": "id-123", "name": "Agent", "type": "INBOX", "purpose": "BUYER",
                "email": "a@b.dev", "scopes": ["mail:read"], "apiKeyPrefix": "loid-abc1",
                "usageCount": 5, "lastUsedAt": None, "createdAt": "2026-01-01T00:00:00Z",
            }))
        client = MailgentPlatform(api_key="mgpk-test")
        result = client.identities.get("id-123")
        assert isinstance(result, IdentityDetail)
        assert result.api_key_prefix == "loid-abc1"
        client.close()

    @respx.mock
    def test_delete(self):
        respx.delete("https://api.mailgent.dev/v0/platform/identities/id-123").mock(
            return_value=httpx.Response(204))
        client = MailgentPlatform(api_key="mgpk-test")
        assert client.identities.delete("id-123") is None
        client.close()

    @respx.mock
    def test_rotate_key(self):
        respx.post("https://api.mailgent.dev/v0/platform/identities/id-123/rotate-key").mock(
            return_value=httpx.Response(200, json={
                "rawKey": "loid-newkey123", "apiKeyPrefix": "loid-newk",
            }))
        client = MailgentPlatform(api_key="mgpk-test")
        result = client.identities.rotate_key("id-123")
        assert isinstance(result, RotateKeyResponse)
        assert result.raw_key.startswith("loid-")
        client.close()

    @respx.mock
    def test_sends_platform_key_in_header(self):
        route = respx.get("https://api.mailgent.dev/v0/platform/identities").mock(
            return_value=httpx.Response(200, json={"identities": [], "count": 0}))
        client = MailgentPlatform(api_key="mgpk-mysecret")
        client.identities.list()
        assert route.calls[0].request.headers["authorization"] == "Bearer mgpk-mysecret"
        client.close()
