from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class MessageResponse:
    message_id: str
    thread_id: str
    inbox_id: str
    from_addrs: list[str]
    to: list[str]
    cc: list[str]
    subject: Optional[str]
    text: Optional[str]
    extracted_text: Optional[str]
    labels: list[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MessageResponse:
        return cls(
            message_id=data["messageId"], thread_id=data["threadId"], inbox_id=data["inboxId"],
            from_addrs=data.get("from", []), to=data.get("to", []), cc=data.get("cc", []),
            subject=data.get("subject"), text=data.get("text"),
            extracted_text=data.get("extractedText"), labels=data.get("labels", []),
            created_at=data["createdAt"],
        )


@dataclass
class ThreadResponse:
    thread_id: str
    inbox_id: str
    subject: Optional[str]
    created_at: str
    updated_at: str
    message_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ThreadResponse:
        return cls(
            thread_id=data["threadId"], inbox_id=data["inboxId"],
            subject=data.get("subject"), created_at=data["createdAt"],
            updated_at=data["updatedAt"], message_count=data.get("messageCount"),
        )


@dataclass
class ThreadDetailResponse:
    thread_id: str
    inbox_id: str
    subject: Optional[str]
    created_at: str
    updated_at: str
    total_messages: int
    messages: list[MessageResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ThreadDetailResponse:
        return cls(
            thread_id=data["threadId"], inbox_id=data["inboxId"],
            subject=data.get("subject"), created_at=data["createdAt"],
            updated_at=data["updatedAt"], total_messages=data.get("totalMessages", 0),
            messages=[MessageResponse.from_dict(m) for m in data.get("messages", [])],
        )


@dataclass
class CredentialMetadata:
    credential_id: str
    type: str
    name: str
    metadata: Optional[dict[str, Any]]
    expires_at: Optional[str]
    last_used_at: Optional[str]
    last_rotated_at: Optional[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CredentialMetadata:
        return cls(
            credential_id=data["credentialId"], type=data["type"], name=data["name"],
            metadata=data.get("metadata"), expires_at=data.get("expiresAt"),
            last_used_at=data.get("lastUsedAt"), last_rotated_at=data.get("lastRotatedAt"),
            created_at=data["createdAt"],
        )


@dataclass
class CredentialWithData(CredentialMetadata):
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CredentialWithData:
        return cls(
            credential_id=data["credentialId"], type=data["type"], name=data["name"],
            metadata=data.get("metadata"), expires_at=data.get("expiresAt"),
            last_used_at=data.get("lastUsedAt"), last_rotated_at=data.get("lastRotatedAt"),
            created_at=data["createdAt"], data=data.get("data", {}),
        )


@dataclass
class IdentityResponse:
    identity_id: str
    name: str
    email: str
    display_name: str
    type: str
    scopes: list[str]
    usage_count: int
    last_used_at: Optional[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentityResponse:
        return cls(
            identity_id=data["identityId"], name=data["name"],
            email=data.get("email", ""), display_name=data.get("displayName", ""),
            type=data["type"], scopes=data.get("scopes", []),
            usage_count=data.get("usageCount", 0), last_used_at=data.get("lastUsedAt"),
            created_at=data["createdAt"],
        )


@dataclass
class IdentitySummary:
    identity_id: str
    name: str
    type: str
    email: Optional[str]
    scopes: list[str]
    usage_count: int
    last_used_at: Optional[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentitySummary:
        return cls(
            identity_id=data["identityId"], name=data["name"], type=data.get("type", "INBOX"),
            email=data.get("email"), scopes=data.get("scopes", []),
            usage_count=data.get("usageCount", 0), last_used_at=data.get("lastUsedAt"),
            created_at=data["createdAt"],
        )


@dataclass
class IdentityDetail(IdentitySummary):
    api_key_prefix: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentityDetail:
        return cls(
            identity_id=data["identityId"], name=data["name"], type=data.get("type", "INBOX"),
            email=data.get("email"), scopes=data.get("scopes", []),
            usage_count=data.get("usageCount", 0), last_used_at=data.get("lastUsedAt"),
            created_at=data["createdAt"], api_key_prefix=data.get("apiKeyPrefix", ""),
        )


@dataclass
class CreateIdentityResponse:
    identity_id: str
    name: str
    type: str
    email_address: str
    scopes: list[str]
    api_key_prefix: str
    raw_key: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CreateIdentityResponse:
        return cls(
            identity_id=data["identityId"], name=data["name"], type=data.get("type", "INBOX"),
            email_address=data["emailAddress"], scopes=data.get("scopes", []),
            api_key_prefix=data["apiKeyPrefix"], raw_key=data["rawKey"],
            created_at=data["createdAt"],
        )


@dataclass
class RotateKeyResponse:
    raw_key: str
    api_key_prefix: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RotateKeyResponse:
        return cls(raw_key=data["rawKey"], api_key_prefix=data["apiKeyPrefix"])


@dataclass
class CalendarEvent:
    event_id: str
    title: str
    description: Optional[str]
    start_at: str
    end_at: Optional[str]
    is_all_day: bool
    location: Optional[str]
    metadata: Optional[dict[str, Any]]
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CalendarEvent:
        return cls(
            event_id=data["eventId"], title=data["title"],
            description=data.get("description"), start_at=data["startAt"],
            end_at=data.get("endAt"), is_all_day=data.get("isAllDay", False),
            location=data.get("location"), metadata=data.get("metadata"),
            created_at=data["createdAt"], updated_at=data["updatedAt"],
        )


@dataclass
class ActivityLog:
    id: str
    action: str
    category: str
    severity: str
    status: str
    description: Optional[str]
    target_type: Optional[str]
    target_id: Optional[str]
    metadata: Optional[dict[str, Any]]
    duration_ms: Optional[int]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ActivityLog:
        return cls(
            id=data["id"], action=data["action"], category=data["category"],
            severity=data["severity"], status=data["status"],
            description=data.get("description"), target_type=data.get("targetType"),
            target_id=data.get("targetId"), metadata=data.get("metadata"),
            duration_ms=data.get("durationMs"), created_at=data["createdAt"],
        )


@dataclass
class LogsStats:
    total: int
    today: int
    errors: int
    by_category: dict[str, int]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LogsStats:
        return cls(total=data["total"], today=data["today"], errors=data["errors"],
                   by_category=data.get("byCategory", {}))


@dataclass
class TotpResponse:
    code: str
    remaining: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TotpResponse:
        return cls(code=data["code"], remaining=data["remaining"])


@dataclass
class DidDocument:
    id: str
    context: list[str]
    also_known_as: list[str] = field(default_factory=list)
    verification_method: list[dict[str, Any]] = field(default_factory=list)
    authentication: list[str] = field(default_factory=list)
    assertion_method: list[str] = field(default_factory=list)
    service: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DidDocument:
        return cls(
            id=data["id"], context=data.get("@context", []),
            also_known_as=data.get("alsoKnownAs", []),
            verification_method=data.get("verificationMethod", []),
            authentication=data.get("authentication", []),
            assertion_method=data.get("assertionMethod", []),
            service=data.get("service", []),
        )
