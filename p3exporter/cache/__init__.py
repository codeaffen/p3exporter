from functools import lru_cache, wraps
from datetime import datetime, timedelta

def timed_lru_cache(lifetime: int = 3600, maxsize: int = 128):
    """Provide cache with a given lifetime.

    This function has to be used as decorator.

    Each time the the cache will be accessed the decorator checks current date is past experation date.
    If so, the cache will cleared and the new expiration data will be recomputed. If not the cache entry
    will be delivered.

    :param lifetime: The lifetime of cache in seconds, defaults to 3600
    :type lifetime: int, optional
    :param maxsize: The maximum number of cache items, defaults to 128
    :type maxsize: int, optional
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=lifetime)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
