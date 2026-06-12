from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional, TypedDict, Union


VaultCredentialType = Literal[
    "LOGIN", "API_KEY", "OAUTH", "TOTP", "SSH_KEY",
    "DATABASE", "SMTP", "AWS", "CERTIFICATE",
    "CARD", "SHIPPING_ADDRESS", "CUSTOM",
]


class ApiKeySecretData(TypedDict):
    """Single API key / secret credential data."""
    key: str


class ApiKeyClientPairData(TypedDict):
    """OAuth-style client credentials (client id + secret)."""
    clientId: str
    secret: str


class CardData(TypedDict, total=False):
    """Payment card stored as an encrypted credential.

    This is password-manager-style secret storage, not a payment processor.
    """
    cardholder: str
    number: str
    expMonth: str
    expYear: str
    cvc: str
    zip: str


class CardMetadata(TypedDict, total=False):
    brand: str
    last4: str


class ShippingAddressData(TypedDict, total=False):
    """Shipping / mailing address stored as an encrypted credential."""
    name: str
    line1: str
    line2: str
    city: str
    state: str
    postcode: str
    country: str
    phone: str


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


#: Project role as returned by the API. ``"BUYER"`` is the default.
IdentityPurpose = Literal["BUYER"]


@dataclass
class IdentityResponse:
    identity_id: str
    name: str
    email: str
    display_name: str
    type: str
    #: Project role as returned by the API. BUYER is the default.
    purpose: IdentityPurpose
    scopes: list[str]
    usage_count: int
    last_used_at: Optional[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentityResponse:
        return cls(
            identity_id=data["identityId"], name=data["name"],
            email=data.get("email", ""), display_name=data.get("displayName", ""),
            type=data["type"], purpose=data["purpose"],
            scopes=data.get("scopes", []),
            usage_count=data.get("usageCount", 0), last_used_at=data.get("lastUsedAt"),
            created_at=data["createdAt"],
        )


@dataclass
class IdentitySummary:
    identity_id: str
    name: str
    type: str
    purpose: IdentityPurpose
    email: Optional[str]
    scopes: list[str]
    usage_count: int
    last_used_at: Optional[str]
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IdentitySummary:
        return cls(
            identity_id=data["identityId"], name=data["name"], type=data.get("type", "INBOX"),
            purpose=data["purpose"],
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
            purpose=data["purpose"],
            email=data.get("email"), scopes=data.get("scopes", []),
            usage_count=data.get("usageCount", 0), last_used_at=data.get("lastUsedAt"),
            created_at=data["createdAt"], api_key_prefix=data.get("apiKeyPrefix", ""),
        )


@dataclass
class CreateIdentityResponse:
    identity_id: str
    name: str
    type: str
    purpose: IdentityPurpose
    email_address: str
    scopes: list[str]
    api_key_prefix: str
    raw_key: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CreateIdentityResponse:
        return cls(
            identity_id=data["identityId"], name=data["name"], type=data.get("type", "INBOX"),
            purpose=data["purpose"],
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
    backup_codes_remaining: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TotpResponse:
        return cls(
            code=data["code"],
            remaining=data["remaining"],
            backup_codes_remaining=data.get("backupCodesRemaining", 0),
        )


@dataclass
class TotpBackupResponse:
    """One single-use TOTP backup code, atomically consumed server-side."""
    code: str
    remaining: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TotpBackupResponse:
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


@dataclass
class PaymentEndpointSummary:
    id: str
    url_pattern: str
    price_usdc: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentEndpointSummary:
        return cls(
            id=data["id"],
            url_pattern=data["urlPattern"],
            price_usdc=data["priceUsdc"],
        )


@dataclass
class PaymentSummary:
    """A row from ``GET /v0/payments``.

    ``amount_usdc_raw`` is raw USDC units (6 decimals); divide by
    1_000_000 for the decimal value. ``status`` is one of ``settled``,
    ``verified``, ``failed``, or ``unpaid_delivered``.
    """

    id: str
    endpoint_id: Optional[str]
    endpoint: Optional[PaymentEndpointSummary]
    network: str
    payer_address: str
    recipient_address: str
    amount_usdc_raw: str
    tx_hash: Optional[str]
    status: str
    resource_url: str
    failure_reason: Optional[str]
    created_at: str
    settled_at: Optional[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentSummary:
        ep = data.get("endpoint")
        return cls(
            id=data["id"],
            endpoint_id=data.get("endpointId"),
            endpoint=PaymentEndpointSummary.from_dict(ep) if ep else None,
            network=data["network"],
            payer_address=data["payerAddress"],
            recipient_address=data["recipientAddress"],
            amount_usdc_raw=data["amountUsdcRaw"],
            tx_hash=data.get("txHash"),
            status=data["status"],
            resource_url=data["resourceUrl"],
            failure_reason=data.get("failureReason"),
            created_at=data["createdAt"],
            settled_at=data.get("settledAt"),
        )


@dataclass
class PaymentReceiptBody:
    version: int
    payment_in_id: str
    endpoint_id: Optional[str]
    identity_id: str
    payer_address: str
    recipient_address: str
    amount_usdc_raw: str
    network: str
    tx_hash: str
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentReceiptBody:
        return cls(
            version=data["version"],
            payment_in_id=data["paymentInId"],
            endpoint_id=data.get("endpointId"),
            identity_id=data["identityId"],
            payer_address=data["payerAddress"],
            recipient_address=data["recipientAddress"],
            amount_usdc_raw=data["amountUsdcRaw"],
            network=data["network"],
            tx_hash=data["txHash"],
            timestamp=data["timestamp"],
        )


@dataclass
class PaymentReceipt:
    """Ed25519-signed receipt — proof of payment for a settled x402 call.

    ``public_key`` is multibase-encoded (``z6Mk…``). ``did`` is the URI
    of the signing Identity, e.g. ``did:web:mailgent.dev:identities:id-…``.
    """

    body: PaymentReceiptBody
    signature: str
    public_key: str
    did: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentReceipt:
        return cls(
            body=PaymentReceiptBody.from_dict(data["body"]),
            signature=data["signature"],
            public_key=data["publicKey"],
            did=data["did"],
        )


@dataclass
class PaymentDetail:
    """A single payment from ``GET /v0/payments/:id`` with the full
    Ed25519-signed receipt and authorization nonce."""

    id: str
    endpoint_id: Optional[str]
    endpoint: Optional[PaymentEndpointSummary]
    network: str
    payer_address: str
    recipient_address: str
    amount_usdc_raw: str
    authorization_nonce: str
    tx_hash: Optional[str]
    status: str
    resource_url: str
    failure_reason: Optional[str]
    created_at: str
    settled_at: Optional[str]
    signed_receipt: PaymentReceipt

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaymentDetail:
        ep = data.get("endpoint")
        return cls(
            id=data["id"],
            endpoint_id=data.get("endpointId"),
            endpoint=PaymentEndpointSummary.from_dict(ep) if ep else None,
            network=data["network"],
            payer_address=data["payerAddress"],
            recipient_address=data["recipientAddress"],
            amount_usdc_raw=data["amountUsdcRaw"],
            authorization_nonce=data["authorizationNonce"],
            tx_hash=data.get("txHash"),
            status=data["status"],
            resource_url=data["resourceUrl"],
            failure_reason=data.get("failureReason"),
            created_at=data["createdAt"],
            settled_at=data.get("settledAt"),
            signed_receipt=PaymentReceipt.from_dict(data["signedReceipt"]),
        )


@dataclass
class SlackConnection:
    """Status of the project's Slack workspace connection."""
    connected: bool
    team_id: Optional[str] = None
    team_name: Optional[str] = None
    bot_user_id: Optional[str] = None
    slack_scopes: Optional[list[str]] = None
    installed_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SlackConnection:
        return cls(
            connected=data["connected"], team_id=data.get("teamId"),
            team_name=data.get("teamName"), bot_user_id=data.get("botUserId"),
            slack_scopes=data.get("slackScopes"), installed_at=data.get("installedAt"),
        )


@dataclass
class SlackConnectResponse:
    """Short-lived OAuth install link — open ``install_url`` in a browser to
    connect a Slack workspace."""
    install_url: str
    expires_in_seconds: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SlackConnectResponse:
        return cls(
            install_url=data["installUrl"],
            expires_in_seconds=data["expiresInSeconds"],
            message=data["message"],
        )


@dataclass
class SlackChannel:
    id: str
    name: str
    is_private: bool
    bot_is_member: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SlackChannel:
        return cls(
            id=data["id"], name=data["name"],
            is_private=data.get("isPrivate", False),
            bot_is_member=data.get("botIsMember", False),
        )


@dataclass
class SlackSendMessageResponse:
    """Acknowledgement for a sent Slack message — ``ts`` doubles as the
    thread anchor for replies."""
    channel: str
    ts: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SlackSendMessageResponse:
        return cls(channel=data["channel"], ts=data["ts"])


@dataclass
class SlackMessage:
    id: str
    channel_id: str
    user_id: str
    text: str
    ts: str
    thread_ts: Optional[str]
    event_type: str
    received_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SlackMessage:
        return cls(
            id=data["id"], channel_id=data["channelId"], user_id=data["userId"],
            text=data.get("text", ""), ts=data["ts"], thread_ts=data.get("threadTs"),
            event_type=data["eventType"], received_at=data["receivedAt"],
        )


@dataclass
class SocialAccount:
    """A social media account connected via the console."""
    id: str
    platform: str
    username: str
    display_name: str
    connected_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SocialAccount:
        return cls(
            id=data["id"], platform=data["platform"],
            username=data.get("username", ""), display_name=data.get("displayName", ""),
            connected_at=data["connectedAt"],
        )


@dataclass
class CreateSocialPostResponse:
    post_id: str
    status: str
    accounts: list[Any]
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CreateSocialPostResponse:
        return cls(
            post_id=data["postId"], status=data["status"],
            accounts=data.get("accounts", []), message=data.get("message", ""),
        )


# --- x402 buyer-side: pay() params, error codes, and response shape ---
#
# Returned as a dict (not a dataclass) to preserve the discriminated-union
# shape — branch on ``result["ok"]``. The TypedDicts give type checkers a
# usable view without forcing a parse step.

PAYMENT_ERROR_CODES = {
    "MANDATE_NOT_FOUND": "mandate_not_found",
    "MANDATE_EXPIRED": "mandate_expired",
    "MANDATE_REVOKED": "mandate_revoked",
    "MANDATE_DAILY_CAP_EXCEEDED": "mandate_daily_cap_exceeded",
    "MANDATE_PER_CALL_EXCEEDED": "mandate_per_call_exceeded",
    "SESSION_KEY_NOT_INSTALLED": "session_key_not_installed",
    "SESSION_KEY_INSTALL_FAILED": "session_key_install_failed",
    "WALLET_NOT_PROVISIONED": "wallet_not_provisioned",
    "BALANCE_INSUFFICIENT": "balance_insufficient",
    "URL_NOT_X402": "url_not_x402",
    "NETWORK_UNSUPPORTED": "network_unsupported",
    "NETWORK_MISMATCH": "network_mismatch",
    "PAYMENT_RESPONSE_INVALID": "payment_response_invalid",
    "SETTLE_FAILED": "settle_failed",
    "FACILITATOR_UNAVAILABLE": "facilitator_unavailable",
    "PAYMENTS_DISABLED": "payments_disabled",
    "UNAUTHORIZED": "unauthorized",
}

PaymentErrorCode = Literal[
    "mandate_not_found",
    "mandate_expired",
    "mandate_revoked",
    "mandate_daily_cap_exceeded",
    "mandate_per_call_exceeded",
    "session_key_not_installed",
    "session_key_install_failed",
    "wallet_not_provisioned",
    "balance_insufficient",
    "url_not_x402",
    "network_unsupported",
    "network_mismatch",
    "payment_response_invalid",
    "settle_failed",
    "facilitator_unavailable",
    "payments_disabled",
    "unauthorized",
]


class PaymentsPayCost(TypedDict):
    amountUsdc: str
    amountUsdcRaw: str
    network: str


class PaymentsPayBalanceAfter(TypedDict):
    usdc: str
    usdcRaw: str


class PaymentsPayMandate(TypedDict):
    mandateId: str
    spentTodayUsdcRaw: str
    dailyCapUsdcRaw: str
    remainingTodayUsdcRaw: str
    validUntil: str


class PaymentsPaySuccess(TypedDict, total=False):
    """Returned when ``ok`` is True. ``content`` is the parsed JSON body
    from the paid API when ``application/json``; ``contentText`` carries the
    raw body otherwise."""
    ok: Literal[True]
    status: int
    content: Any
    contentText: str
    contentType: str
    cost: PaymentsPayCost
    txHash: Optional[str]
    payer: str
    recipient: str
    resource: str
    balanceAfter: PaymentsPayBalanceAfter
    mandate: PaymentsPayMandate
    receipt: Any


class PaymentsPayFailureCost(TypedDict):
    amountUsdc: str
    network: str


class PaymentsPayFailure(TypedDict, total=False):
    """Returned when ``ok`` is False. ``code`` is a stable identifier from
    :data:`PAYMENT_ERROR_CODES`; ``hint`` is a one-line remediation."""
    ok: Literal[False]
    code: PaymentErrorCode
    message: str
    hint: str
    retryAfterMs: int
    resource: str
    cost: PaymentsPayFailureCost


PaymentsPayResponse = Union[PaymentsPaySuccess, PaymentsPayFailure]


class PaymentsPayParams(TypedDict, total=False):
    url: str
    dryRun: bool


# --- Bank-statement-style activity feed (payments out + in, merged) ---


class _PaymentActivityCommon(TypedDict):
    id: str
    network: str
    amountUsdcRaw: str
    counterparty: str
    resource: Optional[str]
    txHash: Optional[str]
    status: str
    failureReason: Optional[str]
    createdAt: str


class PaymentActivityEndpoint(TypedDict):
    id: str
    urlPattern: str


class PaymentActivityIn(_PaymentActivityCommon, total=False):
    direction: Literal["in"]
    endpointId: Optional[str]
    endpoint: Optional[PaymentActivityEndpoint]


class PaymentActivityOut(_PaymentActivityCommon, total=False):
    direction: Literal["out"]
    mandateId: Optional[str]


PaymentActivityRow = Union[PaymentActivityIn, PaymentActivityOut]


class PaymentActivityList(TypedDict):
    activity: list[PaymentActivityRow]
    count: int


# --- Mandates: spend policy attached to a project's wallet ---


class MandateCreateParams(TypedDict, total=False):
    maxPerCallUsdc: str
    dailyCapUsdc: str
    network: str
    validUntil: str


class Mandate(TypedDict, total=False):
    mandateId: str
    identityId: str
    network: str
    maxPerCallUsdc: str
    dailyCapUsdc: str
    validUntil: str
    sessionKeyAddress: str
    onchainInstalled: bool
    installTxHash: Optional[str]
    installError: Optional[str]
    spentTodayUsdc: str
    remainingTodayUsdc: str
    totalSpentUsdc: str
    callCount: int
    revokedAt: Optional[str]
    createdAt: str


class MandateList(TypedDict):
    mandates: list[Mandate]
