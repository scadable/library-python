from __future__ import annotations

from typing import Any


class ScadableError(Exception):
    """Base exception for all Scadable SDK errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        body: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.body = body
        super().__init__(message)


class AuthenticationError(ScadableError):
    """401 — invalid or missing API key."""


class PermissionError(ScadableError):
    """403 — insufficient permissions."""


class NotFoundError(ScadableError):
    """404 — resource not found."""


class RateLimitError(ScadableError):
    """429 — too many requests."""


class InternalServerError(ScadableError):
    """500+ — server error."""


class ConnectionError(ScadableError):
    """Network or transport failure."""


_STATUS_MAP: dict[int, type[ScadableError]] = {
    401: AuthenticationError,
    403: PermissionError,
    404: NotFoundError,
    429: RateLimitError,
}


def from_response(
    status_code: int, body: dict[str, Any] | None = None
) -> ScadableError:
    """Map an HTTP status code to a typed exception."""
    body = body or {}
    message = body.get("error", body.get("message", f"HTTP {status_code}"))
    if status_code >= 500:
        return InternalServerError(message, status_code=status_code, body=body)
    cls = _STATUS_MAP.get(status_code, ScadableError)
    return cls(message, status_code=status_code, body=body)
