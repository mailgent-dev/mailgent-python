import httpx
import json
import pytest
import respx

from loomal import Loomal, AsyncLoomal
from loomal.types import PaymentDetail, PaymentSummary


CHALLENGE_BODY = {
    "x402Version": 1,
    "accepts": [{
        "scheme": "exact",
        "network": "base",
        "maxAmountRequired": "50000",
        "resource": "https://example.com/api",
        "description": "Test API",
        "mimeType": "",
        "payTo": "0xabc",
        "maxTimeoutSeconds": 60,
        "asset": "0xusdc",
        "extra": {"name": "USD Coin", "version": "2"},
    }],
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
        "did": "did:web:loomal.ai:identities:id-1",
    },
}


class TestPaymentsResource:
    def test_client_has_payments_resource(self):
        client = Loomal(api_key="loid-test")
        assert client.payments is not None
        client.close()

    @respx.mock
    def test_challenge(self):
        route = respx.post("https://api.loomal.ai/v0/payments/challenge").mock(
            return_value=httpx.Response(200, json=CHALLENGE_BODY)
        )
        client = Loomal(api_key="loid-test")
        result = client.payments.challenge(amount="0.05", resource="https://example.com/api")

        assert result["x402Version"] == 1
        assert result["accepts"][0]["maxAmountRequired"] == "50000"

        body = json.loads(route.calls[0].request.content)
        assert body["amount"] == "0.05"
        assert body["network"] == "base"
        assert body["resource"] == "https://example.com/api"
        client.close()

    @respx.mock
    def test_redeem_success(self):
        route = respx.post("https://api.loomal.ai/v0/payments/redeem").mock(
            return_value=httpx.Response(200, json={
                "ok": True,
                "paymentResponse": "base64-response",
                "txHash": "0xtxhash",
                "payer": "0xpayer",
                "paymentInId": "pay-1",
            })
        )
        client = Loomal(api_key="loid-test")
        result = client.payments.redeem(
            payment_header="base64-header",
            resource="https://example.com/api",
            amount="0.05",
        )

        assert result["ok"] is True
        assert result["txHash"] == "0xtxhash"

        body = json.loads(route.calls[0].request.content)
        assert body["paymentHeader"] == "base64-header"
        assert body["amount"] == "0.05"
        assert body["network"] == "base"
        client.close()

    @respx.mock
    def test_redeem_rejection(self):
        respx.post("https://api.loomal.ai/v0/payments/redeem").mock(
            return_value=httpx.Response(200, json={
                "ok": False, "stage": "verify", "reason": "invalid_signature",
            })
        )
        client = Loomal(api_key="loid-test")
        result = client.payments.redeem(
            payment_header="bad",
            resource="https://example.com/api",
            amount="0.05",
        )
        assert result["ok"] is False
        assert result["stage"] == "verify"
        client.close()

    @respx.mock
    def test_list(self):
        respx.get("https://api.loomal.ai/v0/payments").mock(
            return_value=httpx.Response(200, json={"payments": [LIST_ROW], "count": 1})
        )
        client = Loomal(api_key="loid-test")
        result = client.payments.list()

        assert result["count"] == 1
        assert isinstance(result["payments"][0], PaymentSummary)
        assert result["payments"][0].status == "settled"
        client.close()

    @respx.mock
    def test_list_with_limit(self):
        route = respx.get("https://api.loomal.ai/v0/payments").mock(
            return_value=httpx.Response(200, json={"payments": [], "count": 0})
        )
        client = Loomal(api_key="loid-test")
        client.payments.list(limit=50)

        assert "limit=50" in str(route.calls[0].request.url)
        client.close()

    @respx.mock
    def test_get(self):
        respx.get("https://api.loomal.ai/v0/payments/pay-1").mock(
            return_value=httpx.Response(200, json=DETAIL_BODY)
        )
        client = Loomal(api_key="loid-test")
        result = client.payments.get("pay-1")

        assert isinstance(result, PaymentDetail)
        assert result.id == "pay-1"
        assert result.signed_receipt.signature == "base64sig"
        assert result.signed_receipt.public_key == "z6Mkpub"
        assert result.signed_receipt.body.payment_in_id == "pay-1"
        client.close()


class TestAsyncPaymentsResource:
    def test_async_client_has_payments_resource(self):
        client = AsyncLoomal(api_key="loid-test")
        assert client.payments is not None

    @respx.mock
    @pytest.mark.asyncio
    async def test_challenge_async(self):
        respx.post("https://api.loomal.ai/v0/payments/challenge").mock(
            return_value=httpx.Response(200, json=CHALLENGE_BODY)
        )
        client = AsyncLoomal(api_key="loid-test")
        result = await client.payments.challenge(amount="0.05", resource="https://example.com/api")
        assert result["x402Version"] == 1
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_async(self):
        respx.get("https://api.loomal.ai/v0/payments/pay-1").mock(
            return_value=httpx.Response(200, json=DETAIL_BODY)
        )
        client = AsyncLoomal(api_key="loid-test")
        result = await client.payments.get("pay-1")
        assert isinstance(result, PaymentDetail)
        assert result.signed_receipt.did == "did:web:loomal.ai:identities:id-1"
        await client.close()
