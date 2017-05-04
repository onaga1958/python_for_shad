import sys
from functools import wraps


def takes(*args_decor):
    def decorator(function):
        @wraps(function)
        def wrapped(*args_func):
            for farg, darg in zip(args_func, args_decor):
                if not isinstance(farg, darg):
                    raise TypeError

            return function(*args_func)
        return wrapped

    return decorator

exec(sys.stdin.read())
