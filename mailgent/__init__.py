from mailgent.client import Mailgent, AsyncMailgent
from mailgent.platform_client import MailgentPlatform, AsyncMailgentPlatform
from mailgent.types import (
    MessageResponse, ThreadResponse, ThreadDetailResponse,
    VaultCredentialType,
    ApiKeySecretData, ApiKeyClientPairData,
    CardData, CardMetadata, ShippingAddressData,
    CredentialMetadata, CredentialWithData, IdentityResponse,
    IdentitySummary, IdentityDetail, CreateIdentityResponse, RotateKeyResponse,
    CalendarEvent,
    ActivityLog, LogsStats, TotpResponse, TotpBackupResponse, DidDocument,
    PaymentEndpointSummary, PaymentSummary, PaymentReceiptBody,
    PaymentReceipt, PaymentDetail,
    PAYMENT_ERROR_CODES, PaymentErrorCode,
    PaymentsPayParams, PaymentsPaySuccess, PaymentsPayFailure, PaymentsPayResponse,
    PaymentActivityIn, PaymentActivityOut, PaymentActivityRow, PaymentActivityList,
    Mandate, MandateCreateParams, MandateList,
)
from mailgent._errors import MailgentApiError

__version__ = "0.6.2"

__all__ = [
    "Mailgent", "AsyncMailgent",
    "MailgentPlatform", "AsyncMailgentPlatform",
    "MailgentApiError",
    "MessageResponse", "ThreadResponse", "ThreadDetailResponse",
    "VaultCredentialType",
    "ApiKeySecretData", "ApiKeyClientPairData",
    "CardData", "CardMetadata", "ShippingAddressData",
    "CredentialMetadata", "CredentialWithData", "IdentityResponse",
    "IdentitySummary", "IdentityDetail", "CreateIdentityResponse", "RotateKeyResponse",
    "CalendarEvent",
    "ActivityLog", "LogsStats", "TotpResponse", "DidDocument",
    "PaymentEndpointSummary", "PaymentSummary", "PaymentReceiptBody",
    "PaymentReceipt", "PaymentDetail",
    "PAYMENT_ERROR_CODES", "PaymentErrorCode",
    "PaymentsPayParams", "PaymentsPaySuccess", "PaymentsPayFailure", "PaymentsPayResponse",
    "PaymentActivityIn", "PaymentActivityOut", "PaymentActivityRow", "PaymentActivityList",
    "Mandate", "MandateCreateParams", "MandateList",
]
