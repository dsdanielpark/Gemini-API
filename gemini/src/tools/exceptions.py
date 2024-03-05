class AuthError(Exception):
    """Invalid credentials/cookies."""

    pass


class APIError(Exception):
    """Package-level error."""

    pass


class GeminiError(Exception):
    """Unhandled server error."""

    pass


class TimeoutError(GeminiError):
    """Request timeout."""

    pass
