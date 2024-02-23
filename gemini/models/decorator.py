import functools
import time
import requests

def retry(attempts=3, delay=2, backoff=2):
    def retry_decorator(func):
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

def log_method(func):
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

def time_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def handle_errors(func):
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
