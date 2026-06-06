import json
import os

import httpx
import pytest
import respx
from mailgent import AsyncMailgent, Mailgent
from mailgent._errors import MailgentApiError


_STORED = {
    "credentialId": "cred-1",
    "name": "test",
    "type": "API_KEY",
    "metadata": None,
    "expiresAt": None,
    "lastUsedAt": None,
    "lastRotatedAt": None,
    "createdAt": "2026-04-16T00:00:00Z",
}


def _body(route) -> dict:
    return json.loads(route.calls.last.request.content)


class TestVaultStoreHelpers:
    @respx.mock
    def test_store_api_key_string(self):
        route = respx.put("https://api.mailgent.dev/v0/vault/stripe").mock(
            return_value=httpx.Response(200, json=_STORED)
        )
        client = Mailgent(api_key="loid-test")
        client.vault.store_api_key("stripe", "sk_live_abc123")
        body = _body(route)
        assert body["type"] == "API_KEY"
        assert body["data"] == {"key": "sk_live_abc123"}
        assert "clientId" not in (body.get("metadata") or {})
        client.close()

    @respx.mock
    def test_store_api_key_client_pair(self):
        route = respx.put("https://api.mailgent.dev/v0/vault/twitter").mock(
            return_value=httpx.Response(200, json=_STORED)
        )
        client = Mailgent(api_key="loid-test")
        client.vault.store_api_key("twitter", {"clientId": "abc123", "secret": "def456"})
        body = _body(route)
        assert body["type"] == "API_KEY"
        assert body["data"] == {"clientId": "abc123", "secret": "def456"}
        assert body["metadata"]["clientId"] == "abc123"
        client.close()

    @respx.mock
    def test_store_card(self):
        route = respx.put("https://api.mailgent.dev/v0/vault/personal-visa").mock(
            return_value=httpx.Response(200, json={**_STORED, "type": "CARD"})
        )
        client = Mailgent(api_key="loid-test")
        client.vault.store_card("personal-visa", {
            "cardholder": "Jane Doe",
            "number": "4242 4242 4242 4242",
            "expMonth": "12",
            "expYear": "2029",
            "cvc": "123",
            "zip": "94103",
        }, metadata={"brand": "Visa"})
        body = _body(route)
        assert body["type"] == "CARD"
        assert body["data"]["cardholder"] == "Jane Doe"
        assert body["data"]["cvc"] == "123"
        assert body["metadata"]["last4"] == "4242"
        assert body["metadata"]["brand"] == "Visa"
        client.close()

    @respx.mock
    def test_store_shipping_address(self):
        route = respx.put("https://api.mailgent.dev/v0/vault/home").mock(
            return_value=httpx.Response(200, json={**_STORED, "type": "SHIPPING_ADDRESS"})
        )
        client = Mailgent(api_key="loid-test")
        client.vault.store_shipping_address("home", {
            "name": "Autonomous Agent",
            "line1": "1 Demo Way",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US",
            "phone": "+1-555-0100",
        })
        body = _body(route)
        assert body["type"] == "SHIPPING_ADDRESS"
        assert body["data"]["line1"] == "1 Demo Way"
        assert body["data"]["country"] == "US"
        assert body["data"]["phone"] == "+1-555-0100"
        client.close()

    @respx.mock
    def test_generic_store_still_works(self):
        route = respx.put("https://api.mailgent.dev/v0/vault/db").mock(
            return_value=httpx.Response(200, json={**_STORED, "type": "DATABASE"})
        )
        client = Mailgent(api_key="loid-test")
        client.vault.store("db", "DATABASE", {"password": "s3cr3t"}, metadata={"host": "db.example.com"})
        body = _body(route)
        assert body["type"] == "DATABASE"
        assert body["data"]["password"] == "s3cr3t"
        client.close()


class TestVaultTotpSync:
    @respx.mock
    def test_totp_includes_backup_codes_remaining(self):
        respx.get("https://api.mailgent.dev/v0/vault/github-2fa/totp").mock(
            return_value=httpx.Response(200, json={"code": "123456", "remaining": 22, "backupCodesRemaining": 4}))
        client = Mailgent(api_key="loid-test")
        res = client.vault.totp("github-2fa")
        assert res.code == "123456"
        assert res.remaining == 22
        assert res.backup_codes_remaining == 4
        client.close()

    @respx.mock
    def test_totp_defaults_backup_codes_remaining_to_zero(self):
        respx.get("https://api.mailgent.dev/v0/vault/legacy/totp").mock(
            return_value=httpx.Response(200, json={"code": "654321", "remaining": 17}))
        client = Mailgent(api_key="loid-test")
        res = client.vault.totp("legacy")
        assert res.backup_codes_remaining == 0
        client.close()

    @respx.mock
    def test_totp_use_backup_posts_and_returns_parsed_response(self):
        route = respx.post("https://api.mailgent.dev/v0/vault/github-2fa/totp/backup").mock(
            return_value=httpx.Response(200, json={"code": "bk-aaaa-1111", "remaining": 3}))
        client = Mailgent(api_key="loid-test")
        res = client.vault.totp_use_backup("github-2fa")
        assert res.code == "bk-aaaa-1111"
        assert res.remaining == 3
        assert route.called
        client.close()

    @respx.mock
    def test_totp_use_backup_accepts_arbitrary_text_codes(self):
        respx.post("https://api.mailgent.dev/v0/vault/x/totp/backup").mock(
            return_value=httpx.Response(200, json={"code": "letters-AND-123!", "remaining": 0}))
        client = Mailgent(api_key="loid-test")
        res = client.vault.totp_use_backup("x")
        assert res.code == "letters-AND-123!"
        assert res.remaining == 0
        client.close()

    @respx.mock
    def test_totp_use_backup_raises_on_400(self):
        respx.post("https://api.mailgent.dev/v0/vault/drained/totp/backup").mock(
            return_value=httpx.Response(400, json={"error": "bad_request", "message": "No unused backup codes remaining"}))
        client = Mailgent(api_key="loid-test")
        with pytest.raises(MailgentApiError):
            client.vault.totp_use_backup("drained")
        client.close()

    @respx.mock
    def test_totp_use_backup_raises_on_404(self):
        respx.post("https://api.mailgent.dev/v0/vault/missing/totp/backup").mock(
            return_value=httpx.Response(404, json={"error": "not_found", "message": "Credential not found"}))
        client = Mailgent(api_key="loid-test")
        with pytest.raises(MailgentApiError):
            client.vault.totp_use_backup("missing")
        client.close()


class TestVaultTotpAsync:
    @respx.mock
    @pytest.mark.asyncio
    async def test_totp_includes_backup_codes_remaining(self):
        respx.get("https://api.mailgent.dev/v0/vault/github-2fa/totp").mock(
            return_value=httpx.Response(200, json={"code": "123456", "remaining": 22, "backupCodesRemaining": 4}))
        client = AsyncMailgent(api_key="loid-test")
        res = await client.vault.totp("github-2fa")
        assert res.backup_codes_remaining == 4
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_totp_use_backup_posts(self):
        respx.post("https://api.mailgent.dev/v0/vault/github-2fa/totp/backup").mock(
            return_value=httpx.Response(200, json={"code": "bk-cccc-3333", "remaining": 1}))
        client = AsyncMailgent(api_key="loid-test")
        res = await client.vault.totp_use_backup("github-2fa")
        assert res.code == "bk-cccc-3333"
        assert res.remaining == 1
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_totp_use_backup_raises_on_error(self):
        respx.post("https://api.mailgent.dev/v0/vault/drained/totp/backup").mock(
            return_value=httpx.Response(400, json={"error": "bad_request", "message": "No unused backup codes remaining"}))
        client = AsyncMailgent(api_key="loid-test")
        with pytest.raises(MailgentApiError):
            await client.vault.totp_use_backup("drained")
        await client.close()


_has_live = bool(os.environ.get("MAILGENT_API_URL"))


@pytest.mark.skipif(not _has_live, reason="MAILGENT_API_URL not set")
class TestVaultIntegration:
    def _client(self):
        return Mailgent(api_key=os.environ["MAILGENT_API_KEY"], base_url=os.environ["MAILGENT_API_URL"])

    def _cred(self):
        return os.environ.get("MAILGENT_TEST_CRED", "test-totp-python")

    def test_totp_has_backup_codes_remaining(self):
        client = self._client()
        res = client.vault.totp(self._cred())
        assert isinstance(res.code, str) and len(res.code) == 6
        assert isinstance(res.backup_codes_remaining, int)
        assert res.backup_codes_remaining >= 0
        client.close()

    def test_totp_use_backup_consumes_a_code(self):
        client = self._client()
        before = client.vault.totp(self._cred()).backup_codes_remaining
        if before == 0:
            return
        used = client.vault.totp_use_backup(self._cred())
        assert isinstance(used.code, str) and len(used.code) > 0
        assert used.remaining == before - 1
        client.close()

    def test_totp_use_backup_consecutive_codes_differ(self):
        client = self._client()
        before = client.vault.totp(self._cred()).backup_codes_remaining
        if before < 2:
            return
        a = client.vault.totp_use_backup(self._cred())
        b = client.vault.totp_use_backup(self._cred())
        assert a.code != b.code
        client.close()

    def test_totp_use_backup_400_when_exhausted(self):
        client = self._client()
        safety = 20
        while safety > 0:
            safety -= 1
            try:
                client.vault.totp_use_backup(self._cred())
            except MailgentApiError:
                break
        with pytest.raises(MailgentApiError):
            client.vault.totp_use_backup(self._cred())
        client.close()

    def test_totp_use_backup_404_for_missing(self):
        client = self._client()
        with pytest.raises(MailgentApiError):
            client.vault.totp_use_backup("__definitely_not_real__")
        client.close()
