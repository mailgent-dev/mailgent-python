from __future__ import annotations

import os
from typing import Optional

from mailgent._http import SyncHttpClient, AsyncHttpClient, DEFAULT_BASE_URL
from mailgent.resources.platform_identities import PlatformIdentitiesResource, AsyncPlatformIdentitiesResource


class MailgentPlatform:
    """Synchronous Mailgent Platform client for identity management."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("MAILGENT_PLATFORM_KEY")
        if not resolved_key:
            raise ValueError("Platform key is required. Pass api_key= or set MAILGENT_PLATFORM_KEY env var.")

        http = SyncHttpClient(
            base_url=base_url or os.environ.get("MAILGENT_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identities = PlatformIdentitiesResource(http)
        self._http = http

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class AsyncMailgentPlatform:
    """Asynchronous Mailgent Platform client for identity management."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("MAILGENT_PLATFORM_KEY")
        if not resolved_key:
            raise ValueError("Platform key is required. Pass api_key= or set MAILGENT_PLATFORM_KEY env var.")

        http = AsyncHttpClient(
            base_url=base_url or os.environ.get("MAILGENT_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identities = AsyncPlatformIdentitiesResource(http)
        self._http = http

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
