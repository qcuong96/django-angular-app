import functools

from django.core.cache import cache


def clear_cache(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        value = func(*args, **kwargs)
        cache.clear()
        return value

    return wrapper_func
