import diskcache as dc
import click
import os

from dash import Dash, html

from const import CacheParams
from utils import AppContainer, HtmlDivRegister


def flush_cache_func():
    cache_dir = CacheParams.CACHE_DIR
    for file in os.listdir(cache_dir):
        os.remove(os.path.join(cache_dir, file))


def init_views():
    """Функция инициализирует модуль views и регистрирует их с помощью
    декораторов таких как HtmlDivRegister"""
    __import__('views')


def init_app(app: Dash):
    cache_dir = CacheParams.CACHE_DIR
    AppContainer(app, dc.Cache(directory=cache_dir))
    init_views()


@click.command()
@click.option('--flush-cache', is_flag=True, default=False,
              help='Starting app with this flag flushes disk cache.')
def start_app(flush_cache: bool):
    if flush_cache is True:
        flush_cache_func()

    app = Dash(__name__)
    init_app(app)
    app.layout = html.Div(HtmlDivRegister().divs)

    app.run_server(debug=True)


if __name__ == '__main__':
    start_app()
