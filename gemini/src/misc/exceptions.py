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
    A specific exception raised when a request to the Gemini server times out.

    Attributes:
        None

    Methods:
        None

    This exception is used to indicate that a network request to the Gemini server did not complete within
    the expected time frame, typically due to network issues or server unresponsiveness.

    Inherits from:
        GeminiAPIError: The base exception class for all Gemini-related API errors.

    Example:
        try:
            response = gemini_client.fetch_data()
        except TimeoutError:
            print("The request to Gemini server timed out.")
    """

    pass


class RateLimitException(Exception):
    """
    Exception raised when a request violates the rate limits of an API.

    This exception should be raised to signal that the calling client has exceeded the allowed number of requests
    in a given time period, as defined by the API's rate limiting policy.

    Attributes:
        None

    Methods:
        None

    Example:
        try:
            check_rate_limit()
        except RateLimitException:
            print("Rate limit exceeded, please try again later.")
    """

    pass


class ContentGenerationException(Exception):
    """
    Exception raised during the failure of content generation processes.

    This exception is intended to be used in scenarios where an automated content generation task fails
    due to internal errors, such as inability to process the input, or failures in underlying services.

    Attributes:
        None

    Methods:
        None

    Example:
        try:
            content = generate_content(input_text)
        except ContentGenerationException:
            print("Failed to generate content due to an internal error.")
    """

    pass
