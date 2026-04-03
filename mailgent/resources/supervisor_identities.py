from __future__ import annotations
from typing import Any, Optional
from mailgent.types import IdentitySummary, IdentityDetail, CreateIdentityResponse, RotateKeyResponse


class SupervisorIdentitiesResource:
    def __init__(self, http):
        self._http = http

    def create(self, name: str, email_name: str, scopes: list[str]) -> CreateIdentityResponse:
        data = self._http.post("/v0/platform/identities", json={
            "name": name, "emailName": email_name, "scopes": scopes,
        })
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

    def delete(self, identity_id: str) -> None:
        self._http.delete(f"/v0/platform/identities/{identity_id}")

    def rotate_key(self, identity_id: str) -> RotateKeyResponse:
        return RotateKeyResponse.from_dict(
            self._http.post(f"/v0/platform/identities/{identity_id}/rotate-key")
        )

    def update_scopes(self, identity_id: str, add_scopes: Optional[list[str]] = None,
                      remove_scopes: Optional[list[str]] = None) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if add_scopes: body["addScopes"] = add_scopes
        if remove_scopes: body["removeScopes"] = remove_scopes
        return self._http.patch(f"/v0/platform/identities/{identity_id}", json=body)


class AsyncSupervisorIdentitiesResource:
    def __init__(self, http):
        self._http = http

    async def create(self, name: str, email_name: str, scopes: list[str]) -> CreateIdentityResponse:
        data = await self._http.post("/v0/platform/identities", json={
            "name": name, "emailName": email_name, "scopes": scopes,
        })
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

    async def delete(self, identity_id: str) -> None:
        await self._http.delete(f"/v0/platform/identities/{identity_id}")

    async def rotate_key(self, identity_id: str) -> RotateKeyResponse:
        return RotateKeyResponse.from_dict(
            await self._http.post(f"/v0/platform/identities/{identity_id}/rotate-key")
        )

    async def update_scopes(self, identity_id: str, add_scopes: Optional[list[str]] = None,
                            remove_scopes: Optional[list[str]] = None) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if add_scopes: body["addScopes"] = add_scopes
        if remove_scopes: body["removeScopes"] = remove_scopes
        return await self._http.patch(f"/v0/platform/identities/{identity_id}", json=body)
