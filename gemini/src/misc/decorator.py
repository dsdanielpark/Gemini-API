import time
import requests
import functools
from typing import Callable


def retry(attempts: int = 3, delay: int = 2, backoff: int = 2) -> Callable:
    """
    Retries a function call with exponential backoff.

    Args:
        attempts (int): The maximum number of attempts. Defaults to 3.
        delay (int): The initial delay in seconds between retries. Defaults to 2.
        backoff (int): The backoff factor. Defaults to 2.

    Returns:
        Callable: Decorator function.
    """

    def retry_decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _attempts, _delay = attempts, delay
            while _attempts > 1:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}, retrying in {_delay} seconds...")
                    time.sleep(_delay)
                    _attempts -= 1
                    _delay *= backoff
            return func(*args, **kwargs)  # Last attempt without catching exceptions

        return wrapper

    return retry_decorator


def log_method(func: Callable) -> Callable:
    """
    Logs method entry and exit.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: Decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        className = args[0].__class__.__name__
        print(f"Entering {className}.{func.__name__}")
        try:
            result = func(*args, **kwargs)
            print(f"Exiting {className}.{func.__name__}")
            return result
        except Exception as e:
            print(f"Exception in {className}.{func.__name__}: {e}")
            raise

    return wrapper


def time_execution(func: Callable) -> Callable:
    """
    Measures the execution time of a function.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: Decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def handle_errors(func: Callable) -> Callable:
    """
    Handles errors that occur during function execution.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: Decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    return wrapper
