from __future__ import annotations
from hivekey.types import IdentityResponse


class IdentityResource:
    def __init__(self, http):
        self._http = http

    def whoami(self) -> IdentityResponse:
        return IdentityResponse.from_dict(self._http.get("/v0/whoami"))


class AsyncIdentityResource:
    def __init__(self, http):
        self._http = http

    async def whoami(self) -> IdentityResponse:
        return IdentityResponse.from_dict(await self._http.get("/v0/whoami"))
