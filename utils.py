from typing import Optional
from dash import Dash


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
    def __init__(self, app: Optional[Dash] = None):
        self.app = app
