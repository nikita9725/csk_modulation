import diskcache as dc
import click

from dash import Dash, html

from utils import AppContainer, HtmlDivRegister


def init_views():
    """Функция инициализирует модуль views и регистрирует их с помощью
    декораторов таких как HtmlDivRegister"""
    __import__('views')


def init_app(app: Dash):
    AppContainer(app, dc.Cache(directory='.cache'))
    init_views()


@click.command()
@click.option('--flush-cache', is_flag=True, default=False,
              help='Starting app with this flag flushes disk cache.')
def start_app(flush_cache: bool):
    app = Dash(__name__)
    init_app(app)
    app.layout = html.Div(HtmlDivRegister().divs)

    if flush_cache is True:
        cache: dc.Cache = AppContainer().cache
        cache.clear()

    app.run_server(debug=True)


if __name__ == '__main__':
    start_app()
