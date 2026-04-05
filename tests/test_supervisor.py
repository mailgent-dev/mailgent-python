import os
import httpx
import pytest
import respx
from hivekey import HivekeySupervisor, AsyncHivekeySupervisor
from hivekey.types import CreateIdentityResponse, IdentityDetail, IdentitySummary, RotateKeyResponse


class TestHivekeySupervisorClient:
    def test_requires_api_key(self):
        os.environ.pop("HIVEKEY_SUPERVISOR_KEY", None)
        with pytest.raises(ValueError, match="Supervisor key is required"):
            HivekeySupervisor()

    def test_creates_with_api_key(self):
        client = HivekeySupervisor(api_key="mgsv-test123")
        assert client.identities is not None
        client.close()

    def test_reads_env_var(self):
        os.environ["HIVEKEY_SUPERVISOR_KEY"] = "mgsv-fromenv"
        try:
            client = HivekeySupervisor()
            assert client.identities is not None
            client.close()
        finally:
            del os.environ["HIVEKEY_SUPERVISOR_KEY"]

    def test_context_manager(self):
        with HivekeySupervisor(api_key="mgsv-test") as client:
            assert client.identities is not None


class TestAsyncHivekeySupervisorClient:
    def test_requires_api_key(self):
        os.environ.pop("HIVEKEY_SUPERVISOR_KEY", None)
        with pytest.raises(ValueError, match="Supervisor key is required"):
            AsyncHivekeySupervisor()


class TestSupervisorIdentitiesResource:
    @respx.mock
    def test_create(self):
        respx.post("https://api.hivekey.ai/v0/platform/identities").mock(
            return_value=httpx.Response(201, json={
                "identityId": "id-123", "name": "Agent", "type": "INBOX",
                "emailAddress": "agent@mailgent.dev", "scopes": ["mail:read"],
                "apiKeyPrefix": "mgent-abc1", "rawKey": "mgent-abc123",
                "createdAt": "2026-01-01T00:00:00Z",
            }))
        client = HivekeySupervisor(api_key="mgsv-test")
        result = client.identities.create("Agent", "agent", ["mail:read"])
        assert isinstance(result, CreateIdentityResponse)
        assert result.identity_id == "id-123"
        assert result.raw_key.startswith("mgent-")
        client.close()

    @respx.mock
    def test_list(self):
        respx.get("https://api.hivekey.ai/v0/platform/identities").mock(
            return_value=httpx.Response(200, json={
                "identities": [{"identityId": "id-1", "name": "Agent", "type": "INBOX",
                                "email": "a@b.dev", "scopes": ["mail:read"],
                                "usageCount": 5, "lastUsedAt": None, "createdAt": "2026-01-01T00:00:00Z"}],
                "count": 1,
            }))
        client = HivekeySupervisor(api_key="mgsv-test")
        result = client.identities.list()
        assert result["count"] == 1
        assert len(result["identities"]) == 1
        assert isinstance(result["identities"][0], IdentitySummary)
        client.close()

    @respx.mock
    def test_get(self):
        respx.get("https://api.hivekey.ai/v0/platform/identities/id-123").mock(
            return_value=httpx.Response(200, json={
                "identityId": "id-123", "name": "Agent", "type": "INBOX",
                "email": "a@b.dev", "scopes": ["mail:read"], "apiKeyPrefix": "mgent-abc1",
                "usageCount": 5, "lastUsedAt": None, "createdAt": "2026-01-01T00:00:00Z",
            }))
        client = HivekeySupervisor(api_key="mgsv-test")
        result = client.identities.get("id-123")
        assert isinstance(result, IdentityDetail)
        assert result.api_key_prefix == "mgent-abc1"
        client.close()

    @respx.mock
    def test_delete(self):
        respx.delete("https://api.hivekey.ai/v0/platform/identities/id-123").mock(
            return_value=httpx.Response(204))
        client = HivekeySupervisor(api_key="mgsv-test")
        assert client.identities.delete("id-123") is None
        client.close()

    @respx.mock
    def test_rotate_key(self):
        respx.post("https://api.hivekey.ai/v0/platform/identities/id-123/rotate-key").mock(
            return_value=httpx.Response(200, json={
                "rawKey": "mgent-newkey123", "apiKeyPrefix": "mgent-newk",
            }))
        client = HivekeySupervisor(api_key="mgsv-test")
        result = client.identities.rotate_key("id-123")
        assert isinstance(result, RotateKeyResponse)
        assert result.raw_key.startswith("mgent-")
        client.close()

    @respx.mock
    def test_sends_supervisor_key_in_header(self):
        route = respx.get("https://api.hivekey.ai/v0/platform/identities").mock(
            return_value=httpx.Response(200, json={"identities": [], "count": 0}))
        client = HivekeySupervisor(api_key="mgsv-mysecret")
        client.identities.list()
        assert route.calls[0].request.headers["authorization"] == "Bearer mgsv-mysecret"
        client.close()
