from mailgent.client import Mailgent, AsyncMailgent
from mailgent.supervisor_client import MailgentSupervisor, AsyncMailgentSupervisor
from mailgent.types import (
    MessageResponse, ThreadResponse, ThreadDetailResponse,
    CredentialMetadata, CredentialWithData, IdentityResponse,
    IdentitySummary, IdentityDetail, CreateIdentityResponse, RotateKeyResponse,
    CalendarEvent,
    ActivityLog, LogsStats, TotpResponse, DidDocument,
)
from mailgent._errors import MailgentError

__version__ = "0.1.0"

__all__ = [
    "Mailgent", "AsyncMailgent",
    "MailgentSupervisor", "AsyncMailgentSupervisor",
    "MailgentError",
    "MessageResponse", "ThreadResponse", "ThreadDetailResponse",
    "CredentialMetadata", "CredentialWithData", "IdentityResponse",
    "IdentitySummary", "IdentityDetail", "CreateIdentityResponse", "RotateKeyResponse",
    "CalendarEvent",
    "ActivityLog", "LogsStats", "TotpResponse", "DidDocument",
]
