import httpx
import respx
from mailgent._http import SyncHttpClient, AsyncHttpClient
from mailgent.resources.mail import MailResource, AsyncMailResource
import pytest


class TestMailRulesSync:
    @respx.mock
    def test_list_rules(self):
        respx.get("https://api.mailgent.dev/v0/email-rules").mock(
            return_value=httpx.Response(200, json={
                "rules": [{"id": "r1", "type": "BLOCK", "scope": "SEND", "value": "*@spam.com", "createdAt": "2026-01-01T00:00:00Z"}]
            }))
        http = SyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = MailResource(http)
        result = mail.list_rules()
        assert len(result["rules"]) == 1
        assert result["rules"][0]["type"] == "BLOCK"
        http.close()

    @respx.mock
    def test_add_rule(self):
        respx.post("https://api.mailgent.dev/v0/email-rules").mock(
            return_value=httpx.Response(201, json={
                "rule": {"id": "r2", "type": "ALLOW", "scope": "RECEIVE", "value": "alice@example.com", "createdAt": "2026-01-01T00:00:00Z"}
            }))
        http = SyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = MailResource(http)
        result = mail.add_rule(type="ALLOW", scope="RECEIVE", value="alice@example.com")
        assert result["rule"]["value"] == "alice@example.com"
        http.close()

    @respx.mock
    def test_delete_rule(self):
        respx.delete("https://api.mailgent.dev/v0/email-rules/rule-123").mock(
            return_value=httpx.Response(204))
        http = SyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = MailResource(http)
        assert mail.delete_rule("rule-123") is None
        http.close()


class TestMailRulesAsync:
    @respx.mock
    @pytest.mark.asyncio
    async def test_list_rules(self):
        respx.get("https://api.mailgent.dev/v0/email-rules").mock(
            return_value=httpx.Response(200, json={
                "rules": [{"id": "r1", "type": "ALLOW", "scope": "RECEIVE", "value": "a@b.com", "createdAt": "2026-01-01T00:00:00Z"}]
            }))
        http = AsyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = AsyncMailResource(http)
        result = await mail.list_rules()
        assert len(result["rules"]) == 1
        await http.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_add_rule(self):
        respx.post("https://api.mailgent.dev/v0/email-rules").mock(
            return_value=httpx.Response(201, json={
                "rule": {"id": "r3", "type": "BLOCK", "scope": "REPLY", "value": "*@spam.com", "createdAt": "2026-01-01T00:00:00Z"}
            }))
        http = AsyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = AsyncMailResource(http)
        result = await mail.add_rule(type="BLOCK", scope="REPLY", value="*@spam.com")
        assert result["rule"]["type"] == "BLOCK"
        await http.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_rule(self):
        respx.delete("https://api.mailgent.dev/v0/email-rules/rule-456").mock(
            return_value=httpx.Response(204))
        http = AsyncHttpClient("https://api.mailgent.dev", "loid-test")
        mail = AsyncMailResource(http)
        assert await mail.delete_rule("rule-456") is None
        await http.close()
