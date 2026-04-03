from __future__ import annotations

import os
from typing import Optional

from mailgent._http import SyncHttpClient, AsyncHttpClient, DEFAULT_BASE_URL
from mailgent.resources.identity import IdentityResource, AsyncIdentityResource
from mailgent.resources.mail import MailResource, AsyncMailResource
from mailgent.resources.vault import VaultResource, AsyncVaultResource
from mailgent.resources.logs import LogsResource, AsyncLogsResource
from mailgent.resources.did import DidResource, AsyncDidResource
from mailgent.resources.calendar import CalendarResource, AsyncCalendarResource


class Mailgent:
    """Synchronous Mailgent API client."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("MAILGENT_API_KEY")
        if not resolved_key:
            raise ValueError("API key is required. Pass api_key= or set MAILGENT_API_KEY env var.")

        http = SyncHttpClient(
            base_url=base_url or os.environ.get("MAILGENT_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identity = IdentityResource(http)
        self.mail = MailResource(http)
        self.vault = VaultResource(http)
        self.logs = LogsResource(http)
        self.did = DidResource(http)
        self.calendar = CalendarResource(http)
        self._http = http

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class AsyncMailgent:
    """Asynchronous Mailgent API client."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("MAILGENT_API_KEY")
        if not resolved_key:
            raise ValueError("API key is required. Pass api_key= or set MAILGENT_API_KEY env var.")

        http = AsyncHttpClient(
            base_url=base_url or os.environ.get("MAILGENT_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identity = AsyncIdentityResource(http)
        self.mail = AsyncMailResource(http)
        self.vault = AsyncVaultResource(http)
        self.logs = AsyncLogsResource(http)
        self.did = AsyncDidResource(http)
        self.calendar = AsyncCalendarResource(http)
        self._http = http

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
