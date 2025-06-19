from functools import lru_cache

def init_cache():
    # No setup needed for lru_cache, but included for interface match
    pass

@lru_cache(maxsize=128)
def expensive_function(x):
    # Replace this with actual expensive computation
    return x * x