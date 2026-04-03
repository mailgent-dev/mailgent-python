from __future__ import annotations
from mailgent.types import DidDocument


class DidResource:
    def __init__(self, http):
        self._http = http

    def resolve(self, identity_id: str) -> DidDocument:
        return DidDocument.from_dict(self._http.get(f"/identities/{identity_id}/did.json"))

    def resolve_domain(self) -> DidDocument:
        return DidDocument.from_dict(self._http.get("/.well-known/did.json"))


class AsyncDidResource:
    def __init__(self, http):
        self._http = http

    async def resolve(self, identity_id: str) -> DidDocument:
        return DidDocument.from_dict(await self._http.get(f"/identities/{identity_id}/did.json"))

    async def resolve_domain(self) -> DidDocument:
        return DidDocument.from_dict(await self._http.get("/.well-known/did.json"))
