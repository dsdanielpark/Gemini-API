class PackageError(Exception):
    """
    Exception raised when encountering invalid credentials or cookies.

    This exception indicates that the provided credentials or cookies are invalid or insufficient for the operation.

    """

    pass


class GeminiAPIError(Exception):
    """
    Exception raised for unhandled errors from the Gemini server.

    This exception indicates that an unexpected error occurred on the Gemini server side, which was not properly handled by the client.

    """

    pass


class TimeoutError(GeminiAPIError):
    """
    Exception raised when a request times out.

    This exception is a subclass of GeminiAPIError and is raised when a request to the Gemini server exceeds the specified timeout period without receiving a response.

    """

    pass
