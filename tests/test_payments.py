import httpx
import json
import pytest
import respx

from mailgent import Mailgent, AsyncMailgent, MailgentApiError
from mailgent.types import PaymentDetail, PaymentSummary


PAY_SUCCESS_BODY = {
    "ok": True,
    "status": 200,
    "content": {"result": "ok"},
    "contentType": "application/json",
    "cost": {"amountUsdc": "0.05", "amountUsdcRaw": "50000", "network": "base"},
    "txHash": "0xtxhash",
    "payer": "0xpayer",
    "recipient": "0xrecipient",
    "resource": "https://api.example.com/search",
    "balanceAfter": {"usdc": "0.95", "usdcRaw": "950000"},
    "mandate": {
        "mandateId": "m-1",
        "spentTodayUsdcRaw": "50000",
        "dailyCapUsdcRaw": "1000000",
        "remainingTodayUsdcRaw": "950000",
        "validUntil": "2027-01-01T00:00:00.000Z",
    },
}

PAY_FAILURE_BODY = {
    "ok": False,
    "code": "mandate_per_call_exceeded",
    "message": "Price 0.50 USDC exceeds maxPerCallUsdc 0.10",
    "hint": "Raise maxPerCallUsdc on the mandate or pay a cheaper endpoint",
    "resource": "https://api.example.com/search",
    "cost": {"amountUsdc": "0.50", "network": "base"},
}

ACTIVITY_BODY = {
    "activity": [
        {
            "id": "po-1",
            "direction": "out",
            "network": "base",
            "amountUsdcRaw": "50000",
            "counterparty": "0xrecipient",
            "resource": "https://api.example.com/search",
            "txHash": "0xtxout",
            "status": "settled",
            "failureReason": None,
            "createdAt": "2026-05-12T10:00:00.000Z",
            "mandateId": "m-1",
        },
        {
            "id": "pi-1",
            "direction": "in",
            "network": "base",
            "amountUsdcRaw": "25000",
            "counterparty": "0xbuyer",
            "resource": "https://you.example.com/api",
            "txHash": "0xtxin",
            "status": "settled",
            "failureReason": None,
            "createdAt": "2026-05-11T09:00:00.000Z",
            "endpointId": "se_abc",
            "endpoint": {"id": "se_abc", "urlPattern": "https://you.example.com/api"},
        },
    ],
    "count": 2,
}


LIST_ROW = {
    "id": "pay-1",
    "endpointId": None,
    "endpoint": None,
    "network": "base",
    "payerAddress": "0xpayer",
    "recipientAddress": "0xrecipient",
    "amountUsdcRaw": "50000",
    "txHash": "0xtxhash",
    "status": "settled",
    "resourceUrl": "https://example.com/api",
    "failureReason": None,
    "createdAt": "2026-04-28T12:34:56.789Z",
    "settledAt": "2026-04-28T12:34:57.123Z",
}

DETAIL_BODY = {
    **LIST_ROW,
    "authorizationNonce": "0xnonce",
    "signedReceipt": {
        "body": {
            "version": 1,
            "paymentInId": "pay-1",
            "endpointId": None,
            "identityId": "id-1",
            "payerAddress": "0xpayer",
            "recipientAddress": "0xrecipient",
            "amountUsdcRaw": "50000",
            "network": "base",
            "txHash": "0xtxhash",
            "timestamp": "2026-04-28T12:34:57.000Z",
        },
        "signature": "base64sig",
        "publicKey": "z6Mkpub",
        "did": "did:web:mailgent.dev:identities:id-1",
    },
}


class TestPaymentsResource:
    def test_client_has_payments_resource(self):
        client = Mailgent(api_key="loid-test")
        assert client.payments is not None
        client.close()

    @respx.mock
    def test_list(self):
        respx.get("https://api.mailgent.dev/v0/payments").mock(
            return_value=httpx.Response(200, json={"payments": [LIST_ROW], "count": 1})
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.list()

        assert result["count"] == 1
        assert isinstance(result["payments"][0], PaymentSummary)
        assert result["payments"][0].status == "settled"
        client.close()

    @respx.mock
    def test_list_with_limit(self):
        route = respx.get("https://api.mailgent.dev/v0/payments").mock(
            return_value=httpx.Response(200, json={"payments": [], "count": 0})
        )
        client = Mailgent(api_key="loid-test")
        client.payments.list(limit=50)

        assert "limit=50" in str(route.calls[0].request.url)
        client.close()

    @respx.mock
    def test_pay_success(self):
        route = respx.post("https://api.mailgent.dev/v0/payments/pay").mock(
            return_value=httpx.Response(200, json=PAY_SUCCESS_BODY)
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.pay(url="https://api.example.com/search")

        assert result["ok"] is True
        assert result["txHash"] == "0xtxhash"
        assert result["cost"]["amountUsdc"] == "0.05"
        assert result["content"] == {"result": "ok"}

        body = json.loads(route.calls[0].request.content)
        assert body["url"] == "https://api.example.com/search"
        assert "dryRun" not in body
        client.close()

    @respx.mock
    def test_pay_failure_pass_through(self):
        respx.post("https://api.mailgent.dev/v0/payments/pay").mock(
            return_value=httpx.Response(402, json=PAY_FAILURE_BODY)
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.pay(url="https://api.example.com/search")

        assert result["ok"] is False
        assert result["code"] == "mandate_per_call_exceeded"
        assert "exceeds maxPerCallUsdc" in result["message"]
        client.close()

    @respx.mock
    def test_pay_forwards_dry_run(self):
        route = respx.post("https://api.mailgent.dev/v0/payments/pay").mock(
            return_value=httpx.Response(200, json=PAY_SUCCESS_BODY)
        )
        client = Mailgent(api_key="loid-test")
        client.payments.pay(url="https://api.example.com/search", dry_run=True)

        body = json.loads(route.calls[0].request.content)
        assert body["dryRun"] is True
        client.close()

    @respx.mock
    def test_pay_raises_on_malformed_body(self):
        respx.post("https://api.mailgent.dev/v0/payments/pay").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized", "message": "missing scope"})
        )
        client = Mailgent(api_key="loid-test")
        with pytest.raises(MailgentApiError, match="discriminator"):
            client.payments.pay(url="https://api.example.com/search")
        client.close()

    @respx.mock
    def test_activity(self):
        route = respx.get("https://api.mailgent.dev/v0/payments/activity").mock(
            return_value=httpx.Response(200, json=ACTIVITY_BODY)
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.activity()

        assert result["count"] == 2
        assert result["activity"][0]["direction"] == "out"
        assert result["activity"][1]["direction"] == "in"
        assert result["activity"][1]["endpoint"]["urlPattern"] == "https://you.example.com/api"
        assert "limit=" not in str(route.calls[0].request.url)
        client.close()

    @respx.mock
    def test_activity_with_limit(self):
        route = respx.get("https://api.mailgent.dev/v0/payments/activity").mock(
            return_value=httpx.Response(200, json={"activity": [], "count": 0})
        )
        client = Mailgent(api_key="loid-test")
        client.payments.activity(limit=25)

        assert "limit=25" in str(route.calls[0].request.url)
        client.close()

    @respx.mock
    def test_mandates_create(self):
        body = {
            "mandateId": "m_abc",
            "identityId": "id-1",
            "network": "base",
            "maxPerCallUsdc": "0.10",
            "dailyCapUsdc": "1.00",
            "validUntil": "2027-01-01T00:00:00.000Z",
            "sessionKeyAddress": "0xsession",
            "onchainInstalled": True,
            "installTxHash": "0xinstall",
            "installError": None,
            "spentTodayUsdc": "0",
            "remainingTodayUsdc": "1.00",
            "totalSpentUsdc": "0",
            "callCount": 0,
            "revokedAt": None,
            "createdAt": "2026-05-12T10:00:00.000Z",
        }
        route = respx.post("https://api.mailgent.dev/v0/payments/mandates").mock(
            return_value=httpx.Response(200, json=body)
        )
        client = Mailgent(api_key="loid-test")
        m = client.payments.mandates.create(
            max_per_call_usdc="0.10",
            daily_cap_usdc="1.00",
        )

        assert m["mandateId"] == "m_abc"
        assert m["installError"] is None

        sent = json.loads(route.calls[0].request.content)
        assert sent["maxPerCallUsdc"] == "0.10"
        assert sent["dailyCapUsdc"] == "1.00"
        assert "network" not in sent  # not forwarded when omitted
        client.close()

    @respx.mock
    def test_mandates_list(self):
        respx.get("https://api.mailgent.dev/v0/payments/mandates").mock(
            return_value=httpx.Response(200, json={"mandates": []})
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.mandates.list()
        assert result == {"mandates": []}
        client.close()

    @respx.mock
    def test_mandates_get_and_revoke(self):
        get_route = respx.get("https://api.mailgent.dev/v0/payments/mandates/m_abc").mock(
            return_value=httpx.Response(200, json={"mandateId": "m_abc"})
        )
        delete_route = respx.delete("https://api.mailgent.dev/v0/payments/mandates/m_abc").mock(
            return_value=httpx.Response(204)
        )
        client = Mailgent(api_key="loid-test")
        m = client.payments.mandates.get("m_abc")
        assert m["mandateId"] == "m_abc"
        client.payments.mandates.revoke("m_abc")

        assert get_route.called
        assert delete_route.called
        client.close()

    @respx.mock
    def test_get(self):
        respx.get("https://api.mailgent.dev/v0/payments/pay-1").mock(
            return_value=httpx.Response(200, json=DETAIL_BODY)
        )
        client = Mailgent(api_key="loid-test")
        result = client.payments.get("pay-1")

        assert isinstance(result, PaymentDetail)
        assert result.id == "pay-1"
        assert result.signed_receipt.signature == "base64sig"
        assert result.signed_receipt.public_key == "z6Mkpub"
        assert result.signed_receipt.body.payment_in_id == "pay-1"
        client.close()


class TestAsyncPaymentsResource:
    def test_async_client_has_payments_resource(self):
        client = AsyncMailgent(api_key="loid-test")
        assert client.payments is not None

    @respx.mock
    @pytest.mark.asyncio
    async def test_pay_async(self):
        respx.post("https://api.mailgent.dev/v0/payments/pay").mock(
            return_value=httpx.Response(200, json=PAY_SUCCESS_BODY)
        )
        client = AsyncMailgent(api_key="loid-test")
        result = await client.payments.pay(url="https://api.example.com/search")
        assert result["ok"] is True
        assert result["txHash"] == "0xtxhash"
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_activity_async(self):
        respx.get("https://api.mailgent.dev/v0/payments/activity").mock(
            return_value=httpx.Response(200, json=ACTIVITY_BODY)
        )
        client = AsyncMailgent(api_key="loid-test")
        result = await client.payments.activity(limit=10)
        assert result["count"] == 2
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_async(self):
        respx.get("https://api.mailgent.dev/v0/payments/pay-1").mock(
            return_value=httpx.Response(200, json=DETAIL_BODY)
        )
        client = AsyncMailgent(api_key="loid-test")
        result = await client.payments.get("pay-1")
        assert isinstance(result, PaymentDetail)
        assert result.signed_receipt.did == "did:web:mailgent.dev:identities:id-1"
        await client.close()
