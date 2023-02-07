from dash import Dash, html

from dash import dcc

from m_code_generator import McodeGenerator
from figures import get_m_code_t_domain_figure


divs = []


# TODO: Настроить декоратор, чтобы можно было передать функции с аргументами
def html_div_register(func):
    divs.append(func())


# TODO: Вынести view в отдельный файл
@html_div_register
def show_m_code():
    m_code_gen = McodeGenerator()
    m_code_t_domain = m_code_gen.get_m_code_in_t_domain()
    fig = get_m_code_t_domain_figure(m_code_t_domain)

    return dcc.Graph(figure=fig)


app = Dash(__name__)
app.layout = html.Div(divs)

app.run_server(debug=True)
