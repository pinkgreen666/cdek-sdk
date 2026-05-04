from typing import Any, Optional


class CdekError(Exception):
    def __init__(
        self, message: str, status_code: Optional[int] = None, response_data: Any = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class CdekAuthError(CdekError):
    """Authentication failed (invalid credentials or token issues)."""

    pass


class CdekValidationError(CdekError):
    """Request validation failed (400 Bad Request)."""

    pass


class CdekNotFoundError(CdekError):
    """Resource not found (404)."""

    pass


class CdekServerError(CdekError):
    """CDEK server error (500, 502, 503, 504)."""

    pass


class CdekRateLimitError(CdekError):
    """Rate limit exceeded (429)."""

    pass


class CdekTimeoutError(CdekError):
    """Request timed out."""

    pass


class CdekNetworkError(CdekError):
    """Network connection error."""

    pass
