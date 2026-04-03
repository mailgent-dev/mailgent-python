class MailgentError(Exception):
    """Raised when the Mailgent API returns a non-2xx response."""

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code

    def __repr__(self) -> str:
        return f"MailgentError(status={self.status}, code={self.code!r}, message={self.args[0]!r})"
