import os
from typing import Callable


def read_cache() -> dict:
    result = dict()
    if os.path.isfile("cache.txt"):
        with open("cache.txt", "r") as cache_file:
            for line in cache_file.readlines():
                parts = line.split(":")
                if not result.get(parts[0]):
                    result[parts[0]] = parts[1][:-1]
    return result


def cache(func: Callable) -> Callable:
    func_name = func.__name__
    global_result = read_cache()

    def inner(*args) -> list:
        one_key_list = [func_name, args]
        one_key = tuple(one_key_list)
        result_inner = global_result.get(one_key)
        if result_inner is None:
            print("Calculating new result")
            result_inner = func(*args)
            global_result[one_key] = result_inner
        else:
            print("Getting from cache")
        save_cache(global_result)
        return result_inner

    return inner


def save_cache(global_result: dict) -> None:
    with open("cache.txt", "a") as cache_file:
        for key, value in global_result.items():
            cache_file.write(str(key) + ":" + str(value) + "\n")
