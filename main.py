import diskcache as dc
from dash import Dash, html

from utils import AppContainer, HtmlDivRegister


def init_views():
    """Функция инициализирует модуль views и регистрирует их с помощью
    декораторов таких как HtmlDivRegister"""
    __import__('views')


def init_app(app: Dash):
    AppContainer(app, dc.Cache(directory='.cache'))
    init_views()


if __name__ == '__main__':
    app = Dash(__name__)
    init_app(app)
    app.layout = html.Div(HtmlDivRegister().divs)

    app.run_server(debug=True)
