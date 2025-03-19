from functools import wraps
from typing import Callable


def read_cache_dict() -> dict:
    result = cache_dict
    return result


def cache(func: Callable) -> Callable:
    func_name = func.__name__

    global cache_dict
    cache_dict = dict()
    global_result = read_cache_dict()

    @wraps(func)
    def wrapper(*args) -> list:
        one_key_list = [func_name, args]
        one_key = tuple(one_key_list)
        result_inner = global_result.get(one_key)
        if result_inner is None:
            print("Calculating new result")
            result_inner = func(*args)
            global_result[one_key] = result_inner
        else:
            print("Getting from cache")
        save_cache_dict(global_result)
        return result_inner

    return wrapper


def save_cache_dict(global_result: dict) -> None:
    for key, value in global_result.items():
        cache_dict[key] = value
