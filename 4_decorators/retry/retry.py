# реализуйте декоратор вида @retry(count: int, delay: timedelta, handled_exceptions: tuple[type(Exceptions)])
import time
from datetime import timedelta
from functools import wraps


def retry(count: int, delay: timedelta, handled_exceptions=(Exception,)):
    if count < 1:
        raise ValueError

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None

            while attempts < count:
                try:
                    return func(*args, **kwargs)
                except handled_exceptions as e:
                    last_exception = e
                    attempts += 1
                    if attempts < count:
                        time.sleep(delay.total_seconds())

            raise last_exception

        return wrapper

    return decorator

