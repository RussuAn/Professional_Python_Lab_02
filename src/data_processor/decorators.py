from functools import wraps
from time import perf_counter


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"Час {func.__name__}: {elapsed:.8f} с")
        return result

    return wrapper
