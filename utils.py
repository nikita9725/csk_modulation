from diskcache import Cache
from typing import Optional
from dash import Dash
from datetime import datetime


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HtmlDivRegister(metaclass=SingletonMeta):
    def __init__(self):
        self.divs = []

    def __call__(self, func):
        def inner(*args, **kwargs):
            self.divs.append(func(*args, **kwargs))
        return inner()


class AppContainer(metaclass=SingletonMeta):
    def __init__(self, app: Optional[Dash] = None,
                 cache_instance: Optional[Cache] = None):
        self.app = app
        self.cache = cache_instance


def evaulation_time_count(func):
    def inner(*args, **kwargs):
        t1 = datetime.now()
        print(f'Evaulation started at: {t1}')
        result = func(*args, **kwargs)
        t2 = datetime.now()
        print(f'Evaulation time: {t2 - t1}')

        return result

    return inner
