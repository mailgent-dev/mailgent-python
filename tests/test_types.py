from hivekey.types import (
    MessageResponse, ThreadDetailResponse, CredentialWithData,
    IdentityResponse, LogsStats, TotpResponse, DidDocument,
)


class TestMessageResponse:
    def test_from_dict(self):
        msg = MessageResponse.from_dict({
            "messageId": "msg-1", "threadId": "thr-1", "inboxId": "inbox@test.dev",
            "from": ["sender@test.dev"], "to": ["recipient@test.dev"], "cc": [],
            "subject": "Hello", "text": "World", "extractedText": None,
            "labels": ["received"], "createdAt": "2026-01-01T00:00:00Z",
        })
        assert msg.message_id == "msg-1"
        assert msg.from_addrs == ["sender@test.dev"]
        assert msg.labels == ["received"]

    def test_missing_optional(self):
        msg = MessageResponse.from_dict({
            "messageId": "msg-2", "threadId": "thr-2", "inboxId": "inbox@test.dev",
            "createdAt": "2026-01-01T00:00:00Z",
        })
        assert msg.from_addrs == []
        assert msg.subject is None


class TestThreadDetailResponse:
    def test_with_messages(self):
        thread = ThreadDetailResponse.from_dict({
            "threadId": "thr-1", "inboxId": "inbox@test.dev", "subject": "Thread",
            "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-02T00:00:00Z",
            "totalMessages": 1,
            "messages": [{"messageId": "msg-1", "threadId": "thr-1", "inboxId": "inbox@test.dev",
                          "from": ["a@b.com"], "to": ["c@d.com"], "cc": [], "subject": "Hi",
                          "text": "Hello", "extractedText": None, "labels": [], "createdAt": "2026-01-01T00:00:00Z"}],
        })
        assert thread.total_messages == 1
        assert len(thread.messages) == 1


class TestCredentialWithData:
    def test_from_dict(self):
        cred = CredentialWithData.from_dict({
            "credentialId": "cred-1", "type": "API_KEY", "name": "stripe",
            "metadata": {"service": "stripe"}, "expiresAt": None,
            "lastUsedAt": None, "lastRotatedAt": None,
            "createdAt": "2026-01-01T00:00:00Z", "data": {"key": "sk_live_xxx"},
        })
        assert cred.data == {"key": "sk_live_xxx"}


class TestIdentityResponse:
    def test_from_dict(self):
        identity = IdentityResponse.from_dict({
            "identityId": "id-123", "name": "Sales", "email": "sales@mailgent.dev",
            "displayName": "Sales Agent", "type": "INBOX",
            "scopes": ["mail:read", "mail:send"], "usageCount": 42,
            "lastUsedAt": "2026-01-01T00:00:00Z", "createdAt": "2025-12-01T00:00:00Z",
        })
        assert identity.identity_id == "id-123"
        assert identity.usage_count == 42


class TestLogsStats:
    def test_from_dict(self):
        stats = LogsStats.from_dict({"total": 100, "today": 5, "errors": 2, "byCategory": {"mail": 80}})
        assert stats.by_category == {"mail": 80}


class TestTotpResponse:
    def test_from_dict(self):
        totp = TotpResponse.from_dict({"code": "123456", "remaining": 15})
        assert totp.code == "123456"


class TestDidDocument:
    def test_from_dict(self):
        doc = DidDocument.from_dict({
            "@context": ["https://www.w3.org/ns/did/v1"], "id": "did:web:api.mailgent.dev",
            "service": [{"id": "#mcp", "type": "MCPServer", "serviceEndpoint": "https://api.hivekey.ai/mcp"}],
        })
        assert doc.id == "did:web:api.mailgent.dev"
        assert len(doc.service) == 1
