from __future__ import annotations
from typing import Any, Optional
from mailgent.types import CreateSocialPostResponse, SocialAccount


class SocialResource:
    """Synchronous ``mailgent.social`` resource.

    Post to connected social media accounts. Accounts are connected in the
    Mailgent console (there is no connect endpoint). Reading requires the
    ``social:read`` scope; posting requires ``social:write``.
    """

    def __init__(self, http):
        self._http = http

    def list_accounts(self) -> dict[str, Any]:
        """List social accounts connected in the console."""
        data = self._http.get("/v0/social/accounts")
        return {"accounts": [SocialAccount.from_dict(a) for a in data.get("accounts", [])]}

    def create_post(self, text: str, account_ids: Optional[list[str]] = None,
                    platforms: Optional[list[str]] = None,
                    media_urls: Optional[list[str]] = None,
                    scheduled_at: Optional[str] = None) -> CreateSocialPostResponse:
        """Publish (or schedule) a post.

        Target specific accounts with ``account_ids``, or whole platforms
        with ``platforms``; omit both to post to every connected account.
        Pass ``scheduled_at`` (ISO 8601) to schedule instead of posting now.
        """
        body: dict[str, Any] = {"text": text}
        if account_ids: body["accountIds"] = account_ids
        if platforms: body["platforms"] = platforms
        if media_urls: body["mediaUrls"] = media_urls
        if scheduled_at: body["scheduledAt"] = scheduled_at
        return CreateSocialPostResponse.from_dict(self._http.post("/v0/social/posts", json=body))

    def list_posts(self, limit: Optional[int] = None) -> dict[str, Any]:
        """List recent posts, newest first."""
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        return self._http.get("/v0/social/posts", params=params or None)

    def get_post(self, post_id: str) -> dict[str, Any]:
        """Get a single post with its per-account delivery results."""
        return self._http.get(f"/v0/social/posts/{post_id}")


class AsyncSocialResource:
    """Asynchronous ``mailgent.social`` resource. Same surface as
    :class:`SocialResource` with ``await`` on each method."""

    def __init__(self, http):
        self._http = http

    async def list_accounts(self) -> dict[str, Any]:
        data = await self._http.get("/v0/social/accounts")
        return {"accounts": [SocialAccount.from_dict(a) for a in data.get("accounts", [])]}

    async def create_post(self, text: str, account_ids: Optional[list[str]] = None,
                          platforms: Optional[list[str]] = None,
                          media_urls: Optional[list[str]] = None,
                          scheduled_at: Optional[str] = None) -> CreateSocialPostResponse:
        body: dict[str, Any] = {"text": text}
        if account_ids: body["accountIds"] = account_ids
        if platforms: body["platforms"] = platforms
        if media_urls: body["mediaUrls"] = media_urls
        if scheduled_at: body["scheduledAt"] = scheduled_at
        return CreateSocialPostResponse.from_dict(await self._http.post("/v0/social/posts", json=body))

    async def list_posts(self, limit: Optional[int] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None: params["limit"] = limit
        return await self._http.get("/v0/social/posts", params=params or None)

    async def get_post(self, post_id: str) -> dict[str, Any]:
        return await self._http.get(f"/v0/social/posts/{post_id}")
