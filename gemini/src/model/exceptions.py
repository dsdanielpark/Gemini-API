class PackageError(Exception):
    """Invalid credentials/cookies."""

    pass


class GeminiAPIError(Exception):
    """Unhandled server error."""

    pass


class TimeoutError(GeminiAPIError):
    """Request timeout."""

    pass
