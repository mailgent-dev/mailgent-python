from __future__ import annotations

from typing import Any, Optional

from mailgent._errors import MailgentApiError
from mailgent.types import (
    Mandate,
    MandateList,
    PaymentActivityList,
    PaymentDetail,
    PaymentSummary,
    PaymentsPayResponse,
)


class MandatesResource:
    """Spend policy attached to your project's wallet. Mailgent enforces the
    caps server-side on every ``payments.pay()`` call. First create takes
    10–30 seconds while the session key lands on Base. If ``installError``
    comes back set, the mandate is unusable — retry creation.

    Mounted at ``mailgent.payments.mandates``.
    """

    def __init__(self, http):
        self._http = http

    def create(
        self,
        max_per_call_usdc: str,
        daily_cap_usdc: str,
        network: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Mandate:
        body: dict[str, Any] = {
            "maxPerCallUsdc": max_per_call_usdc,
            "dailyCapUsdc": daily_cap_usdc,
        }
        if network is not None: body["network"] = network
        if valid_until is not None: body["validUntil"] = valid_until
        return self._http.post("/v0/payments/mandates", json=body)

    def list(self) -> MandateList:
        return self._http.get("/v0/payments/mandates")

    def get(self, mandate_id: str) -> Mandate:
        return self._http.get(f"/v0/payments/mandates/{mandate_id}")

    def revoke(self, mandate_id: str) -> None:
        return self._http.delete(f"/v0/payments/mandates/{mandate_id}")


class AsyncMandatesResource:
    """Async sibling of :class:`MandatesResource`."""

    def __init__(self, http):
        self._http = http

    async def create(
        self,
        max_per_call_usdc: str,
        daily_cap_usdc: str,
        network: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Mandate:
        body: dict[str, Any] = {
            "maxPerCallUsdc": max_per_call_usdc,
            "dailyCapUsdc": daily_cap_usdc,
        }
        if network is not None: body["network"] = network
        if valid_until is not None: body["validUntil"] = valid_until
        return await self._http.post("/v0/payments/mandates", json=body)

    async def list(self) -> MandateList:
        return await self._http.get("/v0/payments/mandates")

    async def get(self, mandate_id: str) -> Mandate:
        return await self._http.get(f"/v0/payments/mandates/{mandate_id}")

    async def revoke(self, mandate_id: str) -> None:
        return await self._http.delete(f"/v0/payments/mandates/{mandate_id}")


class PaymentsResource:
    """Synchronous ``mailgent.payments`` resource.

    Wraps the buyer payments REST endpoints. ``pay`` returns a raw dict
    because the API response is variant-shaped (either ``{ok: true, ...}``
    or ``{ok: false, code, ...}`` — branch on ``result["ok"]``).

    Spend policy lives at ``mailgent.payments.mandates``.
    """

    def __init__(self, http):
        self._http = http
        self.mandates = MandatesResource(http)

    def pay(self, url: str, dry_run: Optional[bool] = None) -> PaymentsPayResponse:
        """Pay any x402-protected URL. Drives the full handshake on your
        project's wallet: discover the 402 challenge, check mandate caps,
        sign EIP-3009, retry, record. Returns a discriminated dict — branch
        on ``result["ok"]``.

        Requires the ``payments:spend`` scope on the API key.
        """
        body: dict[str, Any] = {"url": url}
        if dry_run is not None: body["dryRun"] = dry_run
        data = self._http.post_unchecked("/v0/payments/pay", json=body)
        if not isinstance(data, dict) or "ok" not in data:
            raise MailgentApiError(
                status=0,
                code="unexpected_response",
                message="payments.pay returned a body without an `ok` discriminator",
            )
        return data  # type: ignore[return-value]

    def list(self, limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        data = self._http.get("/v0/payments", params=params or None)
        return {
            "payments": [PaymentSummary.from_dict(p) for p in data.get("payments", [])],
            "count": data["count"],
        }

    def activity(self, limit: Optional[int] = None) -> PaymentActivityList:
        """Bank-statement-style activity feed for the authenticated identity —
        merges payments received (``direction == "in"``) and sent
        (``direction == "out"``), latest first. No scope required.
        """
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        return self._http.get("/v0/payments/activity", params=params or None)

    def get(self, payment_id: str) -> PaymentDetail:
        return PaymentDetail.from_dict(self._http.get(f"/v0/payments/{payment_id}"))


class AsyncPaymentsResource:
    """Asynchronous ``mailgent.payments`` resource. Same surface as
    :class:`PaymentsResource` with ``await`` on each method."""

    def __init__(self, http):
        self._http = http
        self.mandates = AsyncMandatesResource(http)

    async def pay(self, url: str, dry_run: Optional[bool] = None) -> PaymentsPayResponse:
        body: dict[str, Any] = {"url": url}
        if dry_run is not None: body["dryRun"] = dry_run
        data = await self._http.post_unchecked("/v0/payments/pay", json=body)
        if not isinstance(data, dict) or "ok" not in data:
            raise MailgentApiError(
                status=0,
                code="unexpected_response",
                message="payments.pay returned a body without an `ok` discriminator",
            )
        return data  # type: ignore[return-value]

    async def list(self, limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        data = await self._http.get("/v0/payments", params=params or None)
        return {
            "payments": [PaymentSummary.from_dict(p) for p in data.get("payments", [])],
            "count": data["count"],
        }

    async def activity(self, limit: Optional[int] = None) -> PaymentActivityList:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        return await self._http.get("/v0/payments/activity", params=params or None)

    async def get(self, payment_id: str) -> PaymentDetail:
        return PaymentDetail.from_dict(await self._http.get(f"/v0/payments/{payment_id}"))
