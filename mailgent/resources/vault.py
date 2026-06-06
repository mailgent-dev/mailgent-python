from __future__ import annotations
from typing import Any, Optional, Union
from mailgent.types import (
    ApiKeyClientPairData,
    CardData,
    CardMetadata,
    CredentialMetadata,
    CredentialWithData,
    ShippingAddressData,
    TotpBackupResponse,
    TotpResponse,
)


def _last4(card_number: str) -> str:
    return card_number.replace(" ", "").replace("-", "")[-4:]


class VaultResource:
    def __init__(self, http):
        self._http = http

    def list(self) -> dict[str, Any]:
        data = self._http.get("/v0/vault")
        return {"credentials": [CredentialMetadata.from_dict(c) for c in data.get("credentials", [])], "count": data["count"]}

    def get(self, name: str) -> CredentialWithData:
        return CredentialWithData.from_dict(self._http.get(f"/v0/vault/{name}"))

    def store(self, name: str, type: str, data: dict[str, Any],
              metadata: Optional[dict[str, Any]] = None, expires_at: Optional[str] = None) -> CredentialMetadata:
        body: dict[str, Any] = {"type": type, "data": data}
        if metadata: body["metadata"] = metadata
        if expires_at: body["expiresAt"] = expires_at
        return CredentialMetadata.from_dict(self._http.put(f"/v0/vault/{name}", json=body))

    def store_api_key(self, name: str, secret_or_pair: Union[str, ApiKeyClientPairData],
                      metadata: Optional[dict[str, Any]] = None,
                      expires_at: Optional[str] = None) -> CredentialMetadata:
        """Store an API_KEY credential.

        Pass a string for single-secret keys (e.g. ``sk_live_...``), or
        ``{"clientId": ..., "secret": ...}`` for OAuth-style client credentials.
        """
        meta: dict[str, Any] = dict(metadata or {})
        if isinstance(secret_or_pair, str):
            data: dict[str, Any] = {"key": secret_or_pair}
        else:
            data = {"clientId": secret_or_pair["clientId"], "secret": secret_or_pair["secret"]}
            meta["clientId"] = secret_or_pair["clientId"]
        return self.store(name, "API_KEY", data, metadata=meta, expires_at=expires_at)

    def store_card(self, name: str, card: CardData,
                   metadata: Optional[CardMetadata] = None,
                   expires_at: Optional[str] = None) -> CredentialMetadata:
        """Store a CARD credential. Card data is AES-256-GCM encrypted at rest."""
        meta: dict[str, Any] = {"last4": _last4(card["number"])} if card.get("number") else {}
        if metadata:
            meta.update(metadata)
        return self.store(name, "CARD", dict(card), metadata=meta, expires_at=expires_at)

    def store_shipping_address(self, name: str, address: ShippingAddressData,
                               metadata: Optional[dict[str, Any]] = None,
                               expires_at: Optional[str] = None) -> CredentialMetadata:
        """Store a SHIPPING_ADDRESS credential. All fields are encrypted at rest."""
        return self.store(name, "SHIPPING_ADDRESS", dict(address), metadata=metadata, expires_at=expires_at)

    def delete(self, name: str) -> None:
        self._http.delete(f"/v0/vault/{name}")

    def totp(self, name: str) -> TotpResponse:
        return TotpResponse.from_dict(self._http.get(f"/v0/vault/{name}/totp"))

    def totp_use_backup(self, name: str) -> TotpBackupResponse:
        """Atomically consume one single-use TOTP backup code.

        The popped code is moved server-side from ``data.backupCodes`` into
        ``data.usedBackupCodes`` (audit trail) and returned. Raises on 400
        when no codes remain.
        """
        return TotpBackupResponse.from_dict(self._http.post(f"/v0/vault/{name}/totp/backup"))


class AsyncVaultResource:
    def __init__(self, http):
        self._http = http

    async def list(self) -> dict[str, Any]:
        data = await self._http.get("/v0/vault")
        return {"credentials": [CredentialMetadata.from_dict(c) for c in data.get("credentials", [])], "count": data["count"]}

    async def get(self, name: str) -> CredentialWithData:
        return CredentialWithData.from_dict(await self._http.get(f"/v0/vault/{name}"))

    async def store(self, name: str, type: str, data: dict[str, Any],
                    metadata: Optional[dict[str, Any]] = None, expires_at: Optional[str] = None) -> CredentialMetadata:
        body: dict[str, Any] = {"type": type, "data": data}
        if metadata: body["metadata"] = metadata
        if expires_at: body["expiresAt"] = expires_at
        return CredentialMetadata.from_dict(await self._http.put(f"/v0/vault/{name}", json=body))

    async def store_api_key(self, name: str, secret_or_pair: Union[str, ApiKeyClientPairData],
                            metadata: Optional[dict[str, Any]] = None,
                            expires_at: Optional[str] = None) -> CredentialMetadata:
        meta: dict[str, Any] = dict(metadata or {})
        if isinstance(secret_or_pair, str):
            data: dict[str, Any] = {"key": secret_or_pair}
        else:
            data = {"clientId": secret_or_pair["clientId"], "secret": secret_or_pair["secret"]}
            meta["clientId"] = secret_or_pair["clientId"]
        return await self.store(name, "API_KEY", data, metadata=meta, expires_at=expires_at)

    async def store_card(self, name: str, card: CardData,
                         metadata: Optional[CardMetadata] = None,
                         expires_at: Optional[str] = None) -> CredentialMetadata:
        meta: dict[str, Any] = {"last4": _last4(card["number"])} if card.get("number") else {}
        if metadata:
            meta.update(metadata)
        return await self.store(name, "CARD", dict(card), metadata=meta, expires_at=expires_at)

    async def store_shipping_address(self, name: str, address: ShippingAddressData,
                                     metadata: Optional[dict[str, Any]] = None,
                                     expires_at: Optional[str] = None) -> CredentialMetadata:
        return await self.store(name, "SHIPPING_ADDRESS", dict(address), metadata=metadata, expires_at=expires_at)

    async def delete(self, name: str) -> None:
        await self._http.delete(f"/v0/vault/{name}")

    async def totp(self, name: str) -> TotpResponse:
        return TotpResponse.from_dict(await self._http.get(f"/v0/vault/{name}/totp"))

    async def totp_use_backup(self, name: str) -> TotpBackupResponse:
        """Atomically consume one single-use TOTP backup code (async variant)."""
        return TotpBackupResponse.from_dict(await self._http.post(f"/v0/vault/{name}/totp/backup"))
