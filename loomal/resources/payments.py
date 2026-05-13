from __future__ import annotations

from typing import Any, Optional

from loomal.types import PaymentDetail, PaymentSummary


class PaymentsResource:
    """Synchronous ``loomal.payments`` resource.

    Wraps the four payments REST endpoints. ``challenge`` and ``redeem``
    return raw dicts because the API responses are variant-shaped
    (e.g. the redeem response is either ``{ok: true, ...}`` or
    ``{ok: false, ...}`` — branch on ``result["ok"]``).
    """

    def __init__(self, http):
        self._http = http

    def challenge(
        self,
        amount: str,
        resource: Optional[str] = None,
        description: Optional[str] = None,
        network: str = "base",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"amount": amount, "network": network}
        if resource is not None: body["resource"] = resource
        if description is not None: body["description"] = description
        return self._http.post("/v0/payments/challenge", json=body)

    def redeem(
        self,
        payment_header: str,
        resource: str,
        amount: str,
        network: str = "base",
        description: Optional[str] = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "paymentHeader": payment_header,
            "resource": resource,
            "amount": amount,
            "network": network,
        }
        if description is not None: body["description"] = description
        return self._http.post("/v0/payments/redeem", json=body)

    def list(self, limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        data = self._http.get("/v0/payments", params=params or None)
        return {
            "payments": [PaymentSummary.from_dict(p) for p in data.get("payments", [])],
            "count": data["count"],
        }

    def get(self, payment_id: str) -> PaymentDetail:
        return PaymentDetail.from_dict(self._http.get(f"/v0/payments/{payment_id}"))


class AsyncPaymentsResource:
    """Asynchronous ``loomal.payments`` resource. Same surface as
    :class:`PaymentsResource` with ``await`` on each method."""

    def __init__(self, http):
        self._http = http

    async def challenge(
        self,
        amount: str,
        resource: Optional[str] = None,
        description: Optional[str] = None,
        network: str = "base",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"amount": amount, "network": network}
        if resource is not None: body["resource"] = resource
        if description is not None: body["description"] = description
        return await self._http.post("/v0/payments/challenge", json=body)

    async def redeem(
        self,
        payment_header: str,
        resource: str,
        amount: str,
        network: str = "base",
        description: Optional[str] = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "paymentHeader": payment_header,
            "resource": resource,
            "amount": amount,
            "network": network,
        }
        if description is not None: body["description"] = description
        return await self._http.post("/v0/payments/redeem", json=body)

    async def list(self, limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        data = await self._http.get("/v0/payments", params=params or None)
        return {
            "payments": [PaymentSummary.from_dict(p) for p in data.get("payments", [])],
            "count": data["count"],
        }

    async def get(self, payment_id: str) -> PaymentDetail:
        return PaymentDetail.from_dict(await self._http.get(f"/v0/payments/{payment_id}"))
