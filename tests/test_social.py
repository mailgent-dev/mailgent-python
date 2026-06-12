import httpx
import pytest
import respx
from mailgent import Mailgent, AsyncMailgent
from mailgent.types import CreateSocialPostResponse, SocialAccount


class TestSocialResource:
    @respx.mock
    def test_list_accounts(self):
        respx.get("https://api.mailgent.dev/v0/social/accounts").mock(
            return_value=httpx.Response(200, json={
                "accounts": [{
                    "id": "acc-1", "platform": "twitter", "username": "mailgent",
                    "displayName": "Mailgent", "connectedAt": "2026-06-01T00:00:00Z",
                }],
            }))
        client = Mailgent(api_key="mgnt-test")
        result = client.social.list_accounts()
        assert len(result["accounts"]) == 1
        acc = result["accounts"][0]
        assert isinstance(acc, SocialAccount)
        assert acc.platform == "twitter"
        assert acc.username == "mailgent"
        client.close()

    @respx.mock
    def test_create_post(self):
        route = respx.post("https://api.mailgent.dev/v0/social/posts").mock(
            return_value=httpx.Response(201, json={
                "postId": "post-1", "status": "published",
                "accounts": ["acc-1"], "message": "Posted to 1 account",
            }))
        client = Mailgent(api_key="mgnt-test")
        result = client.social.create_post("We just shipped v2!")
        assert isinstance(result, CreateSocialPostResponse)
        assert result.post_id == "post-1"
        assert result.status == "published"
        assert result.accounts == ["acc-1"]
        import json
        body = json.loads(route.calls.last.request.content)
        assert body == {"text": "We just shipped v2!"}
        client.close()

    @respx.mock
    def test_create_post_with_options(self):
        route = respx.post("https://api.mailgent.dev/v0/social/posts").mock(
            return_value=httpx.Response(201, json={
                "postId": "post-2", "status": "scheduled",
                "accounts": ["acc-1", "acc-2"], "message": "Scheduled",
            }))
        client = Mailgent(api_key="mgnt-test")
        result = client.social.create_post(
            "Launch day!",
            platforms=["twitter", "linkedin"],
            media_urls=["https://example.com/banner.png"],
            scheduled_at="2026-07-01T09:00:00Z",
        )
        assert result.status == "scheduled"
        import json
        body = json.loads(route.calls.last.request.content)
        assert body["platforms"] == ["twitter", "linkedin"]
        assert body["mediaUrls"] == ["https://example.com/banner.png"]
        assert body["scheduledAt"] == "2026-07-01T09:00:00Z"
        assert "accountIds" not in body
        client.close()

    @respx.mock
    def test_list_posts(self):
        respx.get("https://api.mailgent.dev/v0/social/posts").mock(
            return_value=httpx.Response(200, json={
                "posts": [{"postId": "post-1", "status": "published"}],
            }))
        client = Mailgent(api_key="mgnt-test")
        result = client.social.list_posts(limit=5)
        assert len(result["posts"]) == 1
        assert result["posts"][0]["postId"] == "post-1"
        client.close()

    @respx.mock
    def test_get_post(self):
        respx.get("https://api.mailgent.dev/v0/social/posts/post-1").mock(
            return_value=httpx.Response(200, json={
                "post": {"postId": "post-1", "status": "published"},
                "results": [{"accountId": "acc-1", "status": "ok"}],
            }))
        client = Mailgent(api_key="mgnt-test")
        result = client.social.get_post("post-1")
        assert result["post"]["postId"] == "post-1"
        assert result["results"][0]["status"] == "ok"
        client.close()

    def test_client_has_social(self):
        client = Mailgent(api_key="mgnt-test")
        assert client.social is not None
        client.close()


class TestAsyncSocialResource:
    def test_async_client_has_social(self):
        client = AsyncMailgent(api_key="mgnt-test")
        assert client.social is not None

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_post_async(self):
        respx.post("https://api.mailgent.dev/v0/social/posts").mock(
            return_value=httpx.Response(201, json={
                "postId": "post-1", "status": "published",
                "accounts": ["acc-1"], "message": "Posted",
            }))
        client = AsyncMailgent(api_key="mgnt-test")
        result = await client.social.create_post("hello")
        assert result.post_id == "post-1"
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_accounts_async(self):
        respx.get("https://api.mailgent.dev/v0/social/accounts").mock(
            return_value=httpx.Response(200, json={
                "accounts": [{"id": "acc-1", "platform": "linkedin", "username": "mg",
                              "displayName": "MG", "connectedAt": "2026-06-01T00:00:00Z"}],
            }))
        client = AsyncMailgent(api_key="mgnt-test")
        result = await client.social.list_accounts()
        assert result["accounts"][0].platform == "linkedin"
        await client.close()
