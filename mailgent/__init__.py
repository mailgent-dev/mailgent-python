from mailgent.client import Mailgent, AsyncMailgent
from mailgent.types import (
    MessageResponse, ThreadResponse, ThreadDetailResponse,
    CredentialMetadata, CredentialWithData, IdentityResponse,
    ActivityLog, LogsStats, TotpResponse, DidDocument,
)
from mailgent._errors import MailgentError

__version__ = "0.1.0"

__all__ = [
    "Mailgent", "AsyncMailgent", "MailgentError",
    "MessageResponse", "ThreadResponse", "ThreadDetailResponse",
    "CredentialMetadata", "CredentialWithData", "IdentityResponse",
    "ActivityLog", "LogsStats", "TotpResponse", "DidDocument",
]
