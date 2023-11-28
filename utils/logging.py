import datetime
from typing import Callable, Any


def logger(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        print(datetime.datetime.now(), f"Начало работы {func.__name__}, параметры {args},{ kwargs}")
        return func(*args, **kwargs)

    return wrapper
