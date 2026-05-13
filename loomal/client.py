from __future__ import annotations

import os
from typing import Optional

from loomal._http import SyncHttpClient, AsyncHttpClient, DEFAULT_BASE_URL
from loomal.resources.identity import IdentityResource, AsyncIdentityResource
from loomal.resources.mail import MailResource, AsyncMailResource
from loomal.resources.vault import VaultResource, AsyncVaultResource
from loomal.resources.logs import LogsResource, AsyncLogsResource
from loomal.resources.did import DidResource, AsyncDidResource
from loomal.resources.calendar import CalendarResource, AsyncCalendarResource
from loomal.resources.payments import PaymentsResource, AsyncPaymentsResource


class Loomal:
    """Synchronous Loomal API client."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("LOOMAL_API_KEY")
        if not resolved_key:
            raise ValueError("API key is required. Pass api_key= or set LOOMAL_API_KEY env var.")

        http = SyncHttpClient(
            base_url=base_url or os.environ.get("LOOMAL_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identity = IdentityResource(http)
        self.mail = MailResource(http)
        self.vault = VaultResource(http)
        self.logs = LogsResource(http)
        self.did = DidResource(http)
        self.calendar = CalendarResource(http)
        self.payments = PaymentsResource(http)
        self._http = http

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class AsyncLoomal:
    """Asynchronous Loomal API client."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 30.0) -> None:
        resolved_key = api_key or os.environ.get("LOOMAL_API_KEY")
        if not resolved_key:
            raise ValueError("API key is required. Pass api_key= or set LOOMAL_API_KEY env var.")

        http = AsyncHttpClient(
            base_url=base_url or os.environ.get("LOOMAL_API_URL", DEFAULT_BASE_URL),
            api_key=resolved_key, timeout=timeout,
        )
        self.identity = AsyncIdentityResource(http)
        self.mail = AsyncMailResource(http)
        self.vault = AsyncVaultResource(http)
        self.logs = AsyncLogsResource(http)
        self.did = AsyncDidResource(http)
        self.calendar = AsyncCalendarResource(http)
        self.payments = AsyncPaymentsResource(http)
        self._http = http

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
