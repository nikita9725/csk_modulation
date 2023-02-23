from dash import dcc, Dash, Input, Output
from diskcache import Cache

from const import MessageParams
from signal_processing import (
    BerResults,
    CskModulator,
    McodeGenerator,
    get_ber_results,
)
from figures import (
    get_m_code_t_domain_figure,
    get_csk_code_t_domain_figure,
    get_csk_code_ber_figure,
)
from utils import AppContainer, HtmlDivRegister


app: Dash = AppContainer().app
cache: Cache = AppContainer().cache


@HtmlDivRegister()
def show_m_code() -> dcc.Graph:
    m_code_gen = McodeGenerator()
    m_code_t_domain = m_code_gen.get_m_code_t_domain()
    fig = get_m_code_t_domain_figure(m_code_t_domain)

    return dcc.Graph(figure=fig)


@HtmlDivRegister()
def show_csk_code() -> dcc.Graph:
    return dcc.Graph(id='csk-graph-snr-slider')


@HtmlDivRegister()
def show_csk_snr_slider_label() -> str:
    return 'SNR dB'


@HtmlDivRegister()
def show_csk_snr_slider() -> dcc.Slider:
    return dcc.Slider(min=-20, max=20, step=1, value=0, id='snr-slider',
                      tooltip={"placement": "top"})


@app.callback(
    Output('csk-graph-snr-slider', 'figure'),
    Input('snr-slider', 'value'))
def update_csk_code(snr_db: float):
    csk_modulatior = CskModulator(snr_db)
    message = MessageParams.MESSAGE
    csk_t_domain = csk_modulatior.modulate_t_domain(message)
    fig = get_csk_code_t_domain_figure(csk_t_domain)

    fig.update_layout(transition_duration=500)

    return fig


@ HtmlDivRegister()
def show_csk_ber() -> dcc.Graph:
    ber_results: BerResults = get_ber_results()

    fig = get_csk_code_ber_figure(ber_results)

    return dcc.Graph(figure=fig)
