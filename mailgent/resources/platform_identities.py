from __future__ import annotations
from typing import Any, Optional
from mailgent.types import IdentitySummary, IdentityDetail, CreateIdentityResponse, RotateKeyResponse


class PlatformIdentitiesResource:
    def __init__(self, http):
        self._http = http

    def create(
        self,
        *,
        purpose: Optional[str] = None,
        name: Optional[str] = None,
        email_name: Optional[str] = None,
        scopes: Optional[list[str]] = None,
    ) -> CreateIdentityResponse:
        """Create an identity. All fields default — `create()` (no args) creates
        a BUYER identity with a fresh 3-word slug name and matching inbox."""
        body: dict[str, Any] = {}
        if purpose is not None: body["purpose"] = purpose
        if name is not None: body["name"] = name
        if email_name is not None: body["emailName"] = email_name
        if scopes is not None: body["scopes"] = scopes
        data = self._http.post("/v0/platform/identities", json=body)
        return CreateIdentityResponse.from_dict(data)

    def list(self, limit: Optional[int] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if page_token: params["pageToken"] = page_token
        data = self._http.get("/v0/platform/identities", params=params or None)
        return {
            "identities": [IdentitySummary.from_dict(i) for i in data.get("identities", [])],
            "count": data["count"],
            "next_page_token": data.get("nextPageToken"),
        }

    def get(self, identity_id: str) -> IdentityDetail:
        return IdentityDetail.from_dict(self._http.get(f"/v0/platform/identities/{identity_id}"))

    def update(
        self,
        identity_id: str,
        *,
        name: Optional[str] = None,
        add_scopes: Optional[list[str]] = None,
        remove_scopes: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Rename and/or update scopes. The inbox email address is immutable."""
        body: dict[str, Any] = {}
        if name is not None: body["name"] = name
        if add_scopes: body["addScopes"] = add_scopes
        if remove_scopes: body["removeScopes"] = remove_scopes
        return self._http.patch(f"/v0/platform/identities/{identity_id}", json=body)

    def delete(self, identity_id: str) -> None:
        self._http.delete(f"/v0/platform/identities/{identity_id}")

    def rotate_key(self, identity_id: str) -> RotateKeyResponse:
        return RotateKeyResponse.from_dict(
            self._http.post(f"/v0/platform/identities/{identity_id}/rotate-key")
        )

    def update_scopes(self, identity_id: str, add_scopes: Optional[list[str]] = None,
                      remove_scopes: Optional[list[str]] = None) -> dict[str, Any]:
        """Backward-compat alias for `update(identity_id, add_scopes=..., remove_scopes=...)`."""
        return self.update(identity_id, add_scopes=add_scopes, remove_scopes=remove_scopes)


class AsyncPlatformIdentitiesResource:
    def __init__(self, http):
        self._http = http

    async def create(
        self,
        *,
        purpose: Optional[str] = None,
        name: Optional[str] = None,
        email_name: Optional[str] = None,
        scopes: Optional[list[str]] = None,
    ) -> CreateIdentityResponse:
        body: dict[str, Any] = {}
        if purpose is not None: body["purpose"] = purpose
        if name is not None: body["name"] = name
        if email_name is not None: body["emailName"] = email_name
        if scopes is not None: body["scopes"] = scopes
        data = await self._http.post("/v0/platform/identities", json=body)
        return CreateIdentityResponse.from_dict(data)

    async def list(self, limit: Optional[int] = None, page_token: Optional[str] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        if page_token: params["pageToken"] = page_token
        data = await self._http.get("/v0/platform/identities", params=params or None)
        return {
            "identities": [IdentitySummary.from_dict(i) for i in data.get("identities", [])],
            "count": data["count"],
            "next_page_token": data.get("nextPageToken"),
        }

    async def get(self, identity_id: str) -> IdentityDetail:
        return IdentityDetail.from_dict(await self._http.get(f"/v0/platform/identities/{identity_id}"))

    async def update(
        self,
        identity_id: str,
        *,
        name: Optional[str] = None,
        add_scopes: Optional[list[str]] = None,
        remove_scopes: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if name is not None: body["name"] = name
        if add_scopes: body["addScopes"] = add_scopes
        if remove_scopes: body["removeScopes"] = remove_scopes
        return await self._http.patch(f"/v0/platform/identities/{identity_id}", json=body)

    async def delete(self, identity_id: str) -> None:
        await self._http.delete(f"/v0/platform/identities/{identity_id}")

    async def rotate_key(self, identity_id: str) -> RotateKeyResponse:
        return RotateKeyResponse.from_dict(
            await self._http.post(f"/v0/platform/identities/{identity_id}/rotate-key")
        )

    async def update_scopes(self, identity_id: str, add_scopes: Optional[list[str]] = None,
                            remove_scopes: Optional[list[str]] = None) -> dict[str, Any]:
        return await self.update(identity_id, add_scopes=add_scopes, remove_scopes=remove_scopes)
