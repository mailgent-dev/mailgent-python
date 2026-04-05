from __future__ import annotations
from typing import Any, Optional
from hivekey.types import CredentialMetadata, CredentialWithData, TotpResponse


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

    def delete(self, name: str) -> None:
        self._http.delete(f"/v0/vault/{name}")

    def totp(self, name: str) -> TotpResponse:
        return TotpResponse.from_dict(self._http.get(f"/v0/vault/{name}/totp"))


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

    async def delete(self, name: str) -> None:
        await self._http.delete(f"/v0/vault/{name}")

    async def totp(self, name: str) -> TotpResponse:
        return TotpResponse.from_dict(await self._http.get(f"/v0/vault/{name}/totp"))
