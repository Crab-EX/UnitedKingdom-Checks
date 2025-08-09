import time
from functools import wraps

import requests


# Simple rate limiter
def rate_limited(max_calls, period):
    """
    Decorator that limits the number of times a function can be called
    within a specified time period (in seconds).
    """
    calls = 0
    last_reset = time.time()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls, last_reset
            current_time = time.time()
            elapsed = current_time - last_reset

            if elapsed > period:
                calls = 0
                last_reset = current_time

            if calls >= max_calls:
                time.sleep(1)
                calls = 0
                last_reset = current_time
            calls += 1
            # Call the original function and return its result
            return func(*args, **kwargs)

        return wrapper

    return decorator